days =["Mon", "Tue", "Wed", "Thu", "Fri"]
shirts =["S1", "S2", "S3", "S4", "S5"]
pants =["P1", "P2", "P3"]
shalwar =["SQ1", "SQ2"]

def validCheck(day, outfit, assignment, used):
    if (day == "Fri" and outfit[0] != "SQ"):
        return False
    if (day in ["Mon", "Thu"] and outfit[0] != "S"):
        return False
    if (outfit in assignment.values()):
        return False
    if (outfit[0] == "S"):
        if (used[outfit[1]] >= 1 or used[outfit[2]] >= 2):
            return False
    if (outfit[0] == "SQ"):
        if (used[outfit[1]] >= 1):
            return False
    return True

outfits = []
for s in shirts:
    for p in pants:
        outfits.append(("S", s, p))

for sq in shalwar:
    outfits.append(("SQ", sq))


def backtrack(assignment, Used, i):
    if i == len(days):
        print(assignment)
        return

    day = days[i]

    for outfit in outfits:
        if (validCheck(day, outfit, assignment, Used)):
            assignment[day] = outfit

            if (outfit[0] == "S"):
                used[outfit[1]] += 1
                used[outfit[2]] += 1
            else:
                used[outfit[1]] += 1

            backtrack(assignment, Used, i+1)

            if (outfit[0] == "S"):
                used[outfit[1]] -= 1
                used[outfit[2]] -= 1
            else:
                used[outfit[1]] -= 1

            del assignment[day]


used = {**{s: 0 for s in shirts}, **{p: 0 for p in pants}, **{sq: 0 for sq in shalwar}}

backtrack({}, used, 0)
