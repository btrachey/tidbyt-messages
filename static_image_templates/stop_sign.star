load("render.star", "render")
load("encoding/base64.star", "base64")

STOP_SIGN = base64.decode("""
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAIKADAAQAAAABAAAAIAAAAACshmLzAAABAElEQVRYCe3WyxLCIAwFUHH8/19WgpOaUELu8MpGFkpp4J46tjQ9wPbODSwtZSk3pB4qKuHYer/M7EUQLmAonBkAoguYCgcRJmBJOIBoApaGO4gbYEt4B6EAW8MNxAU4Et5AFMDR8AqRQsIF4sn9qO9wwOt25XLPkc9/Oc6T5Hka4xprnGqqcxpAC1QFNKc0Hrdq5LjsO/M1gEJoMjUO/B7NfxrraoAMbl3FDMO4IA1gpYSgoYO/3v85EP4cCAfEb0b8Jz+6KeW7jd+Yr/cBghxBiHDKVIDtiCq8CdiGaISbgOUII7wLWIbohLuAaYQTDgGGEUA4DLgQ1AEb3+de+Qcwppw5QaJmlgAAAABJRU5ErkJggg==
""")

def main():
  return render.Root(
    child = render.Row(
      children = [
        render.Image(src=STOP_SIGN)
      ],
      main_align = "center",
      expanded = True,
    )
  )
