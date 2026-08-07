from rich import print
import webcolors

print(webcolors.name_to_hex("brown"))
sss = str(webcolors.name_to_hex("brown")).upper()
print(sss)
print(f"[{sss}]ss[/{sss}]")
print("[green]ss[/green]")
print("[bold blu]ss[/bold blu]")