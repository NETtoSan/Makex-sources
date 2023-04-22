
cube_select = 0
cube_distance_between = 20
cube_distance_arena = 120
cube = [
    "X", "M", "X", "A", "X", "K", "X", "E", "X"
]

def SelectCube(k):
    global cube, cube_select, cube_distance_arena, cube_distance_between
    if k is not "": cube[cube_select] = f"{cube[cube_select]} <"
    if k == "d": cube[cube_select - 1] = f"{cube[cube_select - 1]}".replace(" <", "")
    if k == "a": cube[cube_select + 1] = f"{cube[cube_select + 1]}".replace(" <", "")
    
def RenderCube():
    print("-----------------------------------")
    print(f"[{'] ['.join(cube)}]")
    print("-----------------------------------")
    


def run_cube():
    global cube_select, cube_distance_between
    RenderCube()
    print(f"\n\nDistance from starting area: {(cube_select + 1) * cube_distance_between} cm")

SelectCube(None)
RenderCube()
while True:
    keys = str(input("\nPress A , D to move a cube from left to right\n> ")).lower()
    print(f"Key {keys} pressed" if keys == "a" or keys == "d" else "Enter key pressed " if keys == "" else "Invalid key")
    cube_select = cube_select + 1 if keys == "d" else cube_select - 1 if keys == "a" else cube_select
    SelectCube(keys)
    if keys is not "": RenderCube()
    if keys is "": run_cube()
    