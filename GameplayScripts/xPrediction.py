from math import *
from winstealer import *
from commons.spells2 import BuffType, Buffs, CCType
from enum import *
from time import time

ping: int = 30
extraDelay: int = 0
hugeValue: float = 100000

currentTime: float = 0

winstealer_script_info = {
    "script": "xPrediction",
    "author": "xAzeal",
    "description": "xPredictions by xAzeal from ponche",
}

def Unit_Champion(game) -> list:
    enemies = []

    for champ in game.champs:
        if (
            champ.isTargetable
            or not champ.is_ally_to(game.player)
        ):
            continue
        enemies.append(champ)               
    return enemies


def Unit_Minion(game) -> list:
    minions = []

    for minion in game.minions:
        if (
            not minion.is_alive
            or not minion.isTargetable
            or minion.is_ally_to(game.player)
        ):
            continue
    if minions:
        minions.append(minions)               
    return minions

enemies: list[Unit_Champion] = []
minions: list[Unit_Minion] = []
Unit_ = []
    

def winstealer_draw_settings(game, ui):
    global ping, extraDelay

    ui.text("xAzeal Prediction v1")
    ui.text("Work in progress")
    ping = ui.dragint("Ping", ping, 0, 200)
    extraDelay = ui.dragint("Extra Delay", extraDelay, 0, 120)


def winstealer_load_cfg(cfg):
    global ping, extraDelay

    ping = cfg.get_int('ping', ping)
    extraDelay = cfg.get_int('extraDelay', extraDelay)


def winstealer_save_cfg(cfg):
    global ping, extraDelay
    
    cfg.set_int('ping', ping)
    cfg.set_int('extraDelay', extraDelay)


class HitChance(IntEnum):
    Impossible = -3
    Collision = -2
    OutOfRange = -1
    Medium = 0
    High = 1
    Immobile = 2

    def GetHitChanceName(hitCHance: 'HitChance') -> str:
        if hitCHance == HitChance.Medium:
            return 'Medium'
        if hitCHance == HitChance.High:
            return 'High'
        if hitCHance == HitChance.Immobile:
            return 'Immobile'


class SkillshotType(Enum):
    SkillshotCone = 0
    SkillshotCircle = 1
    SkillshotLine = 2


class CollisionableObjects(Enum):
    Allies = 0
    Walls = 1
    YasuoWall = 2
    Enemies = 3
    Minions = 4
    Jungles = 5


class PredictionInput():
    def __init__(game, unit: Unit_, fromPos, rangeCheckFrom, useBoundingRadius: bool = True, delay: float = 0, radius: float = 1, angle: float = 1, speed: float = hugeValue, range: float = hugeValue, type: SkillshotType = SkillshotType.SkillshotLine, collision: bool = False, collisionableObjects: list[CollisionableObjects] = []) -> None:
        game.From = fromPos
        game.RangeCheckFrom = rangeCheckFrom
        game.Unit = unit
        game.UseBoundingRadius = useBoundingRadius
        game.Delay = delay
        game.Radius = radius
        game.Angle = angle
        game.Speed = speed
        game.CollisionableObjects = collisionableObjects
        game.Collision = collision
        game.Range = range
        game.Type = type


class PredictionOutput():
    def __init__(game, unitPosition: Vec3, castPosition: Vec3, hitChance: HitChance = HitChance.Impossible, timeToHit: float = 0, aoeTargetsHitCount: int = 0, aoeTargetsHit: list[Unit_] = [], collisionObjects: list[Unit_] = []) -> None:
        game.TimeToHit = timeToHit
        game.UnitPosition = unitPosition
        game.CastPosition = castPosition
        game.HitChance = hitChance
        game.AoeTargetsHitCount = aoeTargetsHitCount
        game.AoeTargetsHit = aoeTargetsHit
        game.CollisionObjects = collisionObjects


class Tracker():
    def __init__(game, id: int) -> None:
        game.id = id
        game.time: float = 0
        game.pos: Vec2 = Vec2(0, 0)
        game.dashing: bool = False
        game.stop: float = 0
        game.path: list[Vec2] = []
        game.moving: bool = False
        game.is_visible: bool = False
        game.visibleTime: float = 0
        game.invisibleTime: float = 0


trackers: list[Tracker] = []


class MEC():
    def GetMec(points: list[Vec2]) -> tuple[Vec2, float]:
        convexHull = MEC.MakeConvexHull(points)
        center, radius = MEC.FindMinimalBoundingCircle(convexHull)

        return center, radius

    def MakeConvexHull(points: list[Vec2]) -> list[Vec2]:
        points = MEC.HullCull(points)
        bestPoint = points[0]
        toRemove = 0
        for i in range(len(points)):
            if points[i].y < bestPoint.y or (points[i].y == bestPoint.y and points[i].x < bestPoint.x):
                bestPoint = points[i]
                toRemove = i
        hull = [bestPoint]
        sweepAngle = 0
        del points[toRemove]
        while True:
            if len(points) == 0:
                break
            x = hull[-1].x
            y = hull[-1].y
            bestAngle = 3600
            bestPoint = points[0]
            toRemove = 0
            for i in range(len(points)):
                testAngle = Utility.AngleValue(x, y, points[i].x, points[i].y)
                if testAngle >= sweepAngle and bestAngle > testAngle:
                    bestAngle = testAngle
                    bestPoint = points[i]
                    toRemove = i
            firstAngle = Utility.AngleValue(x, y, hull[0].x, hull[0].y)
            if firstAngle >= sweepAngle and bestAngle >= firstAngle:
                break
            hull.append(bestPoint)
            del points[toRemove]
            sweepAngle = bestAngle
        return hull

    def HullCull(points: list[Vec2]) -> list[Vec2]:
        result = []
        box = MEC.GetMinMaxBox(points)
        left = box[0]
        right = box[0] + box[2]
        top = box[1]
        bottom = box[1] + box[3]
        for point in points:
            if point.x <= left or point.x >= right or point.y <= top or point.y >= bottom:
                result.append(point)
        return result

    def GetMinMaxBox(points: list[Vec2]) -> list[float]:
        ul, ur, ll, lr = MEC.GetMinMaxCorners(points)
        xMin = ul.x
        yMin = ul.y
        xMax = ur.x
        yMax = lr.y
        if yMin < ur.y:
            yMin = ur.y
        if xMax > lr.x:
            xMax = lr.x
        if xMin < ll.x:
            xMin = ll.x
        if yMax > ll.y:
            yMax = ll.y
        return [xMin, yMin, xMax - xMin, yMax - yMin]

    def GetMinMaxCorners(points: list[Vec2]) -> tuple[Vec2, Vec2, Vec2, Vec2]:
        ul = points[0]
        ur = ul
        ll = ul
        lr = ul
        for point in points:
            if -point.x - point.y > -ul.x - ul.y:
                ul = point
            if point.x - point.y > ur.x - ur.y:
                ur = point
            if -point.x + point.y > -ll.x + ll.y:
                ll = point
            if point.x + point.y > lr.x + lr.y:
                lr = point
        return ul, ur, ll, lr

    def FindMinimalBoundingCircle(points: list[Vec2]) -> tuple[Vec2, float]:
        hull = MEC.MakeConvexHull(points)
        center = points[0]
        radius = hugeValue
        for i in range(len(hull) - 1):
            for j in range(i + 1, len(hull)):
                testCenter = Vec2((hull[i].x + hull[j].x) / 2,
                                  (hull[i].y + hull[j].y) / 2)
                dx = testCenter.x - hull[i].x
                dy = testCenter.y - hull[i].y
                testRadius = dx * dx + dy * dy

                if testRadius < radius:
                    if MEC.CircleEnclosesPoints(testCenter, testRadius, points, i, j, -1):
                        center = testCenter
                        radius = testRadius
        for i in range(len(hull) - 2):
            for j in range(i + 1, len(hull) - 1):
                for k in range(j + 1, len(hull)):
                    testCenter, testRadius = MEC.FindCircle(
                        hull[i], hull[j], hull[k])

                    if testRadius < radius:
                        if MEC.CircleEnclosesPoints(testCenter, testRadius, points, i, j, k):
                            center = testCenter
                            radius = testRadius
        if radius == hugeValue:
            radius = 0
        else:
            radius = sqrt(radius)
        return center, radius

    def CircleEnclosesPoints(center: Vec2, radius: float, points: list[Vec2], skip1: int, skip2: int, skip3: int) -> bool:
        unskipped = []
        for i in range(len(points)):
            if i != skip1 and i != skip2 and i != skip3:
                unskipped.append(points[i])
        enclosing = 0
        for point in unskipped:
            dx = center.x - point.x
            dy = center.y - point.y
            testRadius = dx * dx + dy * dy
            if not testRadius > radius:
                enclosing += 1
        return enclosing == len(unskipped)

    def FindCircle(a: Vec2, b: Vec2, c: Vec2) -> tuple[Vec2, float]:
        x1 = (b.x + a.x) / 2
        y1 = (b.y + a.y) / 2
        dy1 = b.x - a.x
        dx1 = -(b.y - a.y)
        x2 = (c.x + b.x) / 2
        y2 = (c.y + b.y) / 2
        dy2 = c.x - b.x
        dx2 = -(c.y - b.y)
        cx = (y1 * dx1 * dx2 + x2 * dx1 * dy2 - x1 * dy1 *
              dx2 - y2 * dx1 * dx2) / (dx1 * dy2 - dy1 * dx2)
        cy = (cx - x1) * dy1 / dx1 + y1
        center = Vec2(cx, cy)
        dx = cx - a.x
        dy = cy - a.y
        radius = dx * dx + dy * dy
        return center, radius


class Utility():
    def To2D(point: Vec3) -> Vec2:
        return Vec2(point.x, point.z)

    def To3D(point: Vec2, y: float = 0) -> Vec3:
        return Vec3(point.x, y, point.y)

    def IsFacing(source: Unit_, unit: Unit_, angle: float = 90) -> bool:
        sPos = Utility.To2D(source.pos)
        uPos = Utility.To2D(unit.pos)
        dir = Utility.To2D(source.dir)
        return Utility.AngleBetween(sPos, sPos + dir * 65, uPos) < angle

    def AngleBetween(point1: Vec2, point2: Vec2, point3: Vec2) -> float:
        angle = abs(degrees(atan2(point3.y - point1.y, point3.x -
                    point1.x) - atan2(point2.y - point1.y, point2.x - point1.x)))
        if angle < 0:
            angle = angle + 360
        if angle > 180:
            angle = 360 - angle
        return angle

    def AngleValue(x1: float, y1: float, x2: float, y2: float) -> float:
        dx = x2 - x1
        ax = abs(dx)
        dy = y2 - y1
        ay = abs(dy)
        t = ax + ay == 0 and 40 or dy / (ax + ay)
        t = dx < 0 and 2 - t or (dy < 0 and 4 + t or t)
        return t * 90

    def IsInRange(p1: Vec2, p2: Vec2, range: float) -> bool:
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        return dx * dx + dy * dy <= range * range

    def GetPathIndex(path: list[Vec3], unitPos: Vec3):
        bestDistance = hugeValue
        index = -1
        for i in range(1, len(path)):
            distance = path[i].distance(unitPos)
            if distance < bestDistance:
                bestDistance = distance
                index = i
        return index

    def GetPath(unit: Unit_) -> list[Vec2]:
        result = [Utility.To2D(unit.pos)]
        if not unit.moving:
            return result
        if unit.dashing:
            result.append(Utility.To2D(unit.path[-1]))
            return result
        path = unit.path
        index = Utility.GetPathIndex(path, unit.pos)
        if index == -1:
            return result
        for i in range(index, len(path)):
            result.append(Utility.To2D(path[i]))
        return result

    def CutPath(path: list[Vec2], distance: float) -> list[Vec2]:
        if distance <= 0:
            return path
        result = []
        for i in range(len(path) - 1):
            dist = path[i].distance(path[i + 1])
            if dist > distance:
                result.append(Utility.Extended(
                    path[i], Utility.Normalized(path[i + 1], path[i]), distance))
                for j in range(i + 1, len(path)):
                    result.append(path[j])
                break
            distance -= dist
        return result if len(result) > 0 else [path[-1]]

    def Extended(point: Vec2, direction: Vec2, range: float) -> Vec2:
        if direction == None:
            return point
        return Vec2(point.x + direction.x * range, point.y + direction.y * range)

    def MagnitudeSquared(point: Vec2) -> float:
        return point.x * point.x + point.y * point.y

    def Magnitude(point: Vec2) -> float:
        return sqrt(Utility.MagnitudeSquared(point))

    def DotProduct(point1: Vec2, point2: Vec2) -> float:
        return point1.x * point2.x + point1.y * point2.y

    def Interception(startPos: Vec2, endPos: Vec2, source: Vec2, speed: float, moveSpeed: float) -> float:
        dx = endPos.x - startPos.x
        dy = endPos.y - startPos.y
        magnitude = sqrt(dx * dx + dy * dy)
        if magnitude == 0:
            return None
        tx = startPos.x - source.x
        ty = startPos.y - source.y
        tvx = (dx / magnitude) * moveSpeed
        tvy = (dy / magnitude) * moveSpeed
        a = tvx * tvx + tvy * tvy - speed * speed
        b = 2 * (tvx * tx + tvy * ty)
        c = tx * tx + ty * ty
        ts = None
        if abs(a) < 1e-6:
            if abs(b) < 1e-6:
                if abs(c) < 1e-6:
                    ts = Vec2(0, 0)
            else:
                ts = Vec2(-c / b, -c / b)
        else:
            disc = b * b - 4 * a * c
            if disc >= 0:
                disc = sqrt(disc)
                a = 2 * a
                ts = Vec2((-b - disc) / a, (-b + disc) / a)
        sol = None
        if ts:
            t0 = ts.x
            t1 = ts.y
            t = min(t0, t1)
            if t < 0:
                t = max(t0, t1)
            if t > 0:
                sol = t
        return sol

    def GetPredictedPath(source: Vec2, speed: float, moveSpeed: float, path: list[Vec2]) -> tuple[list[Vec2], float]:
        result = []
        tT = 0
        for i in range(len(path) - 1):
            result.append(path[i])
            tB = path[i].distance(path[i + 1]) / moveSpeed
            direction = Utility.Normalized(path[i + 1], path[i])
            a = Utility.Extended(path[i], direction, -(moveSpeed * tT))
            t = Utility.Interception(a, path[i + 1], source, speed, moveSpeed)
            if t and t >= tT and t <= tT + tB:
                result.append(Utility.Extended(a, direction, t * moveSpeed))
                return result, t
            tT += tB
        return None, -1

    def GetReversedPath(path: list[Vec2]) -> list[Vec2]:
        result = []
        for i in range(len(path) - 1, 0, -1):
            result.append(path[i])
        return result

    def GetPing() -> float:
        return ping * 0.001 / 2

    def GetExtraDelay() -> float:
        return extraDelay * 0.001

    def Equals(point1: Vec2, point2: Vec2, distance: float) -> bool:
        return point1.distance(point2) < distance

    def Normalized(point1: Vec2, point2: Vec2) -> Vec2:
        dx = point1.x - point2.x
        dy = point1.y - point2.y
        length = sqrt(dx * dx + dy * dy)
        if length > 0:
            inv = 1.0 / length
            return Vec2(dx * inv, dy * inv)
        return None

    def IsImmobileCC(cc: Buff) -> bool:
        return cc.type_info == CCType.Stun or cc.type_info == CCType.Root or cc.type_info == CCType.Sleep or cc.type_info == CCType.Airbone

    def GetImmobileDuration(target: Unit_Champion) -> float:
        bestStunDuration = 0
        if target.curr_casting and target.curr_casting.remaining > 0:
            bestStunDuration = target.curr_casting.remaining
        for buff in target.buffs:
            b = Buffs.get(buff.name)
            if b.type == BuffType.CC:
                if b.type_info == Utility.IsImmobileCC(b):
                    duration = buff.time_end - currentTime
                    if buff.count > 0 and duration > bestStunDuration:
                        bestStunDuration = duration
        return bestStunDuration

    def GetPathLenght(path: list[Vec2]) -> float:
        result = 0
        for i in range(len(path) - 1):
            result += path[i].distance(path[i + 1])
        return result

    def ClosestPointOnLineSegment(p: Vec2, p1: Vec2, p2: Vec2) -> tuple[Vec2, bool]:
        if Utility.Equals(p, p1, 50) or Utility.Equals(p, p2, 50):
            return p, True
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        t = ((p.x - p1.x) * dx + (p.y - p1.y) * dy) / (dx * dx + dy * dy)
        if t < 0:
            return p1, False
        if t > 1:
            return p2, False
        return Vec2(p1.x + t * dx, p1.y + t * dy), True

    def GetInRange(fromPos: Vec3, enemies: list[Unit_Champion], range: float) -> list[Unit_Champion]:
        result = []
        source = Utility.To2D(fromPos)
        for enemy in enemies:
            if Utility.IsInRange(Utility.To2D(enemy.pos), source, range):
                result.append(enemy)
        return result

    def IsPointInArc(sourcePos: Vec2, unitPos: Vec2, endPos: Vec2, range: float, angle: float) -> bool:
        angle = radians(angle) / 2
        a = sourcePos - unitPos
        b = sourcePos - endPos
        c = Utility.Magnitude(b)
        d = Utility.DotProduct(a, b) / c
        inf = d / Utility.Magnitude(a) <= cos(angle)
        if inf:
            return False
        return d <= c and sourcePos.distance(unitPos) <= range


class Prediction():
    def GetPredictionData(target: Unit_, source: Vec2, speed: float, delay: float, radius: float) -> tuple[Vec2, Vec2, float]:
        index = Prediction.GetTrackerIndex(target.net_id)
        moveSpeed = target.move_speed if target.move_speed > 0 else 315
        if index == -1:
            if len(target.path) == 0 or not target.moving:
                return Utility.To2D(target.pos), Utility.To2D(target.pos), 0
            path = Utility.GetPath(target)
            if len(path) <= 1:
                return Utility.To2D(target.pos), Utility.To2D(target.pos), 0
            fullDelay = delay + Utility.GetPing() + Utility.GetExtraDelay()
            cutPath = Utility.CutPath(path, moveSpeed * fullDelay)
            if speed == hugeValue:
                return cutPath[0], cutPath[0], 0
            predPath, times = Utility.GetPredictedPath(
                source, speed, moveSpeed, path)
            if predPath:
                return predPath[-1], predPath[-1], 0
            return path[-1], path[-1], times
        tracker = trackers[index]
        if tracker.is_visible:
            if time() < tracker.visibleTime + 0.5:
                return None, None, -1
        elif time() > tracker.invisibleTime + 1:
            return None, None, -1
        if tracker.moving and len(tracker.path) <= 1:
            return None, None, -1
        if not tracker.moving:
            pos = Utility.To2D(target.pos)
            return pos, pos, delay + pos.distance(source) / speed
        # if tracker.dashing:
            #pos = Utility.To2D(target.pos)
            # return pos, pos, delay + pos.distance(source) / speed
        fullDelay = delay + Utility.GetPing() + Utility.GetExtraDelay()
        path = Utility.GetPath(target)
        if speed == hugeValue:
            path1 = Utility.CutPath(
                path, moveSpeed * fullDelay)
            path2 = Utility.CutPath(
                path, (moveSpeed * fullDelay) - radius)
            return path1[0], path2[0], delay
        path, times = Utility.GetPredictedPath(source, speed, moveSpeed, Utility.CutPath(
            path, moveSpeed * fullDelay))
        if path:
            path2 = Utility.CutPath(Utility.GetReversedPath(path), radius)
            return path[-1], path2[0], delay + path[-1].distance(source) / speed
        pos = tracker.path[-1]
        return pos, pos, delay + pos.distance(source) / speed

    def GetPrediction(input: PredictionInput) -> PredictionOutput:
        index = Prediction.GetTrackerIndex(input.Unit.net_id)
        if index != -1:
            Prediction.UpdateTracker(input.Unit, index)
        source = Utility.To2D(input.From)
        radius = input.Radius + \
            input.Unit.bounding_radius if input.UseBoundingRadius else input.Radius
        unitPos, castPos, timeToHit = Prediction.GetPredictionData(
            input.Unit, source, input.Speed, input.Delay, radius)
        if not castPos or not unitPos:
            return PredictionOutput(None, None, hitChance=HitChance.Impossible)
        hitChance = Prediction.GetHitChance(
            input, source, unitPos, castPos, timeToHit)
        castPos = Utility.To3D(castPos, input.Unit.pos.y)
        unitPos = Utility.To3D(unitPos, input.Unit.pos.y)
        return PredictionOutput(unitPos, castPos, hitChance, timeToHit)

    def IsHighHitChance(target: Unit_Champion, index: int, duration: float) -> bool:
        tracker = trackers[index]
        if not target.is_visible:
            return False
        if tracker.moving:
            if time() < tracker.time + 0.15:
                return True
            if time() > tracker.time + 1.0 and Utility.GetPathLenght(tracker.path) > 1000:
                return True
            return False
        if time() - tracker.stop < 0.05:
            return True
        if time() - tracker.stop > 1.0:
            return True
        if duration > 0.05:
            return True
        return False

    def IsInRange(rangeFrom: Vec2, castPos: Vec2, unitPos: Vec2, range: float, spellType: SkillshotType) -> bool:
        return Utility.IsInRange(castPos if spellType == SkillshotType.SkillshotCircle else unitPos, rangeFrom, range)

    def ShouldCheckThisCollision(collisionableObjects: list[CollisionableObjects], collision: CollisionableObjects):
        for collisionableObject in collisionableObjects:
            if collision == collisionableObject:
                return True
        return False

    def IsColliding(input: PredictionInput, source: Vec2, castPos: Vec2) -> bool:
        source = Utility.Extended(
            source, Utility.Normalized(source, castPos), 75)
        castPos = Utility.Extended(
            castPos, Utility.Normalized(castPos, castPos), 75)
        unitId = input.Unit.net_id
        collisions = input.CollisionableObjects
        input.Collision = False
        if Prediction.ShouldCheckThisCollision(collisions, CollisionableObjects.Minions):
            for minion in minions:
                if minion.is_visible and minion.net_id != unitId:
                    pos = Utility.To2D(minion.pos)
                    point, isOnSegment = Utility.ClosestPointOnLineSegment(
                        pos, source, castPos)
                    if isOnSegment and Utility.IsInRange(pos, point, input.Radius + 15 + minion.bounding_radius):
                        return True
                    elif minion.moving:
                        input.Unit = minion
                        output = Prediction.GetPrediction(input)
                        if output.UnitPosition:
                            pos = Utility.To2D(output.UnitPosition)
                            point, isOnSegment = Utility.ClosestPointOnLineSegment(
                                pos, source, castPos)
                            if isOnSegment and Utility.IsInRange(pos, point, input.Radius + 15 + minion.bounding_radius):
                                return True
        if Prediction.ShouldCheckThisCollision(collisions, CollisionableObjects.Enemies):
            for enemy in enemies:
                if enemy.is_visible and enemy.net_id != unitId:
                    pos = Utility.To2D(enemy.pos)
                    point, isOnSegment = Utility.ClosestPointOnLineSegment(
                        pos, source, castPos)
                    if isOnSegment and Utility.IsInRange(pos, point, input.Radius + 15 + enemy.bounding_radius):
                        return True
                    elif enemy.moving:
                        input.Unit = enemy
                        output = Prediction.GetPrediction(input)
                        if output.UnitPosition:
                            pos = Utility.To2D(output.UnitPosition)
                            point, isOnSegment = Utility.ClosestPointOnLineSegment(
                                pos, source, castPos)
                            if isOnSegment and Utility.IsInRange(pos, point, input.Radius + 15 + enemy.bounding_radius):
                                return True
        return False

    def GetHitChance(input: PredictionInput, source: Vec2, unitPos: Vec2, castPos: Vec2, timeToHit: float) -> HitChance:
        if not unitPos or not castPos:
            return HitChance.Impossible
        index = Prediction.GetTrackerIndex(input.Unit.net_id)
        hitChance = HitChance.Medium
        if index != -1:
            duration = Utility.GetImmobileDuration(input.Unit)
            if duration > 0:
                if timeToHit < duration:
                    hitChance = HitChance.Immobile
            if hitChance != HitChance.Immobile and Prediction.IsHighHitChance(input.Unit, index, duration):
                hitChance = HitChance.High
        if input.Range != hugeValue and not Prediction.IsInRange(Utility.To2D(input.RangeCheckFrom), castPos, unitPos, input.Range, input.Type):
            return HitChance.Impossible
        if input.Collision and Prediction.IsColliding(input, source, castPos):
            return HitChance.Collision
        return hitChance

    def GetTrackerIndex(unitId: int) -> int:
        for i in range(len(trackers)):
            if trackers[i].id == unitId:
                return i
        return -1

    def UpdateTracker(enemy: Unit_Champion, index: int) -> None:
        global trackers
        if enemy.is_visible:
            if not trackers[index].is_visible:
                trackers[index].is_visible = True
                trackers[index].visibleTime = time()
        else:
            if trackers[index].is_visible:
                trackers[index].is_visible = False
                trackers[index].invisibleTime = time()
        if enemy.path and len(enemy.path) > 0:
            endPos = Utility.To2D(enemy.path[-1])
            if not Utility.Equals(endPos, trackers[index].pos, 50):
                trackers[index].time = time()
            trackers[index].pos = endPos
            trackers[index].dashing = enemy.dashing
        elif trackers[index].moving:
            trackers[index].stop = time()
        trackers[index].path = Utility.GetPath(enemy)
        trackers[index].moving = enemy.moving

    def TrackerHandler() -> None:
        global trackers
        for enemy in enemies:
            trackerIndex = Prediction.GetTrackerIndex(enemy.net_id)
            if trackerIndex == -1:
                trackers.append(Tracker(enemy.net_id))
            else:
                Prediction.UpdateTracker(enemy, trackerIndex)


class AoePrediction():
    def GetPrediction(input: PredictionInput) -> PredictionOutput:
        if input.Type == SkillshotType.SkillshotCircle:
            return AoePrediction.GetPredictionCircle(input)
        if input.Type == SkillshotType.SkillshotLine:
            return AoePrediction.GetPredictionLine(input)
        if input.Type == SkillshotType.SkillshotCone:
            return AoePrediction.GetPredictionAngle(input)

    class Candidate():
        def __init__(game, unit: Unit_, pos: Vec2) -> None:
            game.Unit = unit
            game.Pos = pos

    def GetPossibleUnits(input: PredictionInput) -> list['Candidate']:
        sourcePos = Utility.To2D(input.RangeCheckFrom)
        originalUnitId = input.Unit.net_id
        result = []
        for enemy in enemies:
            if enemy.is_visible and enemy.net_id != originalUnitId and Utility.To2D(enemy.pos).distance(sourcePos) <= input.Range + input.Radius + enemy.bounding_radius:
                input.Unit = enemy
                enemyPred = Prediction.GetPrediction(input)
                if enemyPred.HitChance >= HitChance.Medium:
                    result.append(AoePrediction.Candidate(
                        enemy, Utility.To2D(enemyPred.UnitPosition)))
        return result

    def GetCandidatesPos(candidates: list[Candidate]) -> list[Vec2]:
        result = []
        for candidate in candidates:
            result.append(candidate.Pos)
        return result

    def GetCandidatesUnits(candidates: list[Candidate]) -> list[Unit_]:
        result = []
        for candidate in candidates:
            result.append(candidate.Unit)
        return result

    def SortByDistance(center: Vec2, x: Vec2):
        return center.distance(x)

    def GetPredictionCircle(input: PredictionInput) -> PredictionOutput:
        output = Prediction.GetPrediction(input)
        if not output.HitChance >= HitChance.Medium:
            return output
        bestPos = Utility.To2D(output.CastPosition)
        bestCount = 1
        bestHit = [AoePrediction.Candidate(
            input.Unit, Utility.To2D(output.UnitPosition))]
        sourcePos = Utility.To2D(input.RangeCheckFrom)
        candidates = AoePrediction.GetPossibleUnits(input)
        if len(candidates) > 0:
            candidates.append(AoePrediction.Candidate(
                input.Unit, Utility.To2D(output.UnitPosition)))
            while len(candidates) > 1:
                center, radius = MEC.GetMec(
                    AoePrediction.GetCandidatesPos(candidates))
                if sourcePos.distance(center) <= input.Range and radius <= input.Radius:
                    bestPos = center
                    bestCount = len(candidates)
                    bestHit = candidates
                    break
                candidates = sorted(candidates, key=lambda x: AoePrediction.SortByDistance(
                    center, x.Pos), reverse=True)
                del candidates[0]
        output.CastPosition = Utility.To3D(bestPos, input.Unit.pos.y)
        output.AoeTargetsHitCount = bestCount
        output.AoeTargetsHit = AoePrediction.GetCandidatesUnits(bestHit)
        return output

    def GetPredictionLine(input: PredictionInput) -> PredictionOutput:
        output = Prediction.GetPrediction(input)
        if not output.HitChance >= HitChance.Medium:
            return output
        bestPos = Utility.To2D(output.CastPosition)
        bestCount = 1
        bestHit = [AoePrediction.Candidate(
            input.Unit, Utility.To2D(output.UnitPosition))]
        fromPos = Utility.To2D(input.From)
        candidates = AoePrediction.GetPossibleUnits(input)
        positions = []
        if len(candidates) > 0:
            candidates.append(AoePrediction.Candidate(
                input.Unit, Utility.To2D(output.UnitPosition)))
            for candidate in candidates:
                positions.append(candidate.Pos)
            for i in range(len(candidates)):
                for j in range(len(candidates)):
                    if i != j:
                        pos = Vec2((candidates[i].Pos.x + candidates[j].Pos.x) / 2,
                                   (candidates[i].Pos.y + candidates[j].Pos.y) / 2)
                        positions.append(pos)
            for i in range(len(positions)):
                endPos = positions[i]
                count = 0
                cHit = []
                for j in range(len(candidates)):
                    point, IsOnSegment = Utility.ClosestPointOnLineSegment(
                        candidates[j].Pos, fromPos, endPos)
                    if candidates[j].Pos.distance(point) <= input.Radius + candidates[j].Unit.bounding_radius:
                        cHit.append(candidates[j])
                        count += 1
                if count > bestCount:
                    bestPos = positions[i]
                    bestCount = count
                    bestHit = cHit
        output.CastPosition = Utility.To3D(bestPos, input.Unit.pos.y)
        output.AoeTargetsHitCount = bestCount
        output.AoeTargetsHit = AoePrediction.GetCandidatesUnits(bestHit)
        return output

    def GetPredictionAngle(input: PredictionInput) -> PredictionOutput:
        output = Prediction.GetPrediction(input)
        if not output.HitChance >= HitChance.Medium:
            return output
        bestPos = Utility.To2D(output.CastPosition)
        bestCount = 1
        bestHit = [AoePrediction.Candidate(
            input.Unit, Utility.To2D(output.UnitPosition))]
        fromPos = Utility.To2D(input.From)
        candidates = AoePrediction.GetPossibleUnits(input)
        positions = []
        if len(candidates) > 0:
            candidates.append(AoePrediction.Candidate(
                input.Unit, Utility.To2D(output.UnitPosition)))
            for candidate in candidates:
                positions.append(candidate.Pos)
            for i in range(len(candidates)):
                for j in range(len(candidates)):
                    if i != j:
                        pos = Vec2((candidates[i].Pos.x + candidates[j].Pos.x) / 2,
                                   (candidates[i].Pos.y + candidates[j].Pos.y) / 2)
                        positions.append(pos)

            for i in range(len(positions)):
                endPos = positions[i]
                count = 0
                cHit = []
                for j in range(len(candidates)):
                    if Utility.IsPointInArc(fromPos, candidates[j].Pos, endPos, input.Range, input.Angle):
                        cHit.append(candidates[j])
                        count += 1
                if count > bestCount:
                    bestPos = positions[i]
                    bestCount = count
                    bestHit = cHit
        output.CastPosition = Utility.To3D(bestPos, input.Unit.pos.y)
        output.AoeTargetsHitCount = bestCount
        output.AoeTargetsHit = AoePrediction.GetCandidatesUnits(bestHit)
        return output



def winstealer_update(game, ui):
    global enemies, currentTime, minions

    currentTime = game.time
    enemies = Unit_Champion(game)
    minions = Unit_Minion(game)
    Prediction.TrackerHandler()