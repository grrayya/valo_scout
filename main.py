from analyzer.api_client import ValorantAPI
from analyzer.algorithms import heapsort_matches
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

# Stealth/Blackout aesthetic theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})

console = Console(theme=custom_theme)


def main():
    console.print("\n[info]Initializing ValoScout Subsystems...[/info]")

    api = ValorantAPI()
    console.print("[info]Fetching recent Ascendant/Diamond tier data...[/info]\n")

    # Fetch data
    matches = api.fetch_recent_matches("Player", "NA1")

    # Process data using custom Heapsort
    top_matches = heapsort_matches(matches, sort_key="efficiency_score")[:5]

    # Render Stealth UI Table
    table = Table(title="Top 5 Impact Matches (Omen Main)", style="dim")

    table.add_column("Map", style="cyan", no_wrap=True)
    table.add_column("K/D/A", style="dim white")
    table.add_column("KDA Ratio", justify="right", style="green")
    table.add_column("Utility (Smokes)", justify="right", style="magenta")
    table.add_column("Impact Score", justify="right", style="bold white")

    for match in top_matches:
        kda_str = f"{match['kills']}/{match['deaths']}/{match['assists']}"
        table.add_row(
            match["map"],
            kda_str,
            str(match["kda_ratio"]),
            str(match["smokes_deployed"]),
            str(match["efficiency_score"])
        )

    console.print(table)
    console.print("\n[dim]Systems standby.[/dim]\n")


if __name__ == "__main__":
    main()