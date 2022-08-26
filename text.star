load("render.star", "render")

def main():
  return render.Root(
    delay = <SCROLL_SPEED>,
    child = render.Box(
      render.Marquee(
        height=32,
        scroll_direction="vertical",
        child = render.Row(
          expanded=True,
          main_align="space_evenly",
          cross_align="center",
          children = [
            render.WrappedText(
              content="<MESSAGE_TEXT>",
              align="center",
              color = "#<HEX_COLOR>",
              font = "<FONT>"
            )
          ]
        )
      )
    )
  )
