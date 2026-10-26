from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
class StatisticalAlert:
    def __init__(self) -> None:
        self.organismtypes = ("Plant", "Herb", "Pred", "ApexPredator")
        self.populationhistory = []
        self.events = []
        self.prevcounts = None

    def update(self, event: dict) -> None:
        """process a notification from EventManager.

        Args:
            event: rvent dictionary containing its type and relevant data.
        """
        eventtype = event["type"]

        if eventtype == "turn_finished":
            self._record_population(event)

        elif eventtype == "entity_reproduced":
            self.events.append({
                "turn": event["turn"],
                "event": "Reproduction",
                "description": (
                    f"Herbivore born at {event['position']}"
                ),
            })

        elif eventtype == "entity_eaten":
            eater = type(event["eater"]).__name__
            prey = type(event["prey"]).__name__

            self.events.append({
                "turn": event["turn"],
                "event": "Consumption",
                "description": f"{eater} ate {prey}",
            })

    def _record_population(self, event: dict) -> None:
        """count living organisms and detect population extinction."""
        turn = event["turn"]

        counts = Counter(
            type(entity).__name__
            for entity in event["entities"]
        )

        row = {"turn": turn}

        for organism in self.organismtypes:
            row[organism] = counts[organism]

        self.populationhistory.append(row)

        if self.prevcounts is not None:
            for organism in self.organismtypes:
                if (
                        self.prevcounts[organism] > 0
                        and counts[organism] == 0
                ):
                    self.events.append({
                        "turn": turn,
                        "event": "Extinction",
                        "description": f"{organism} became extinct",
                    })

        self.prevcounts = counts

    def save_results(self, output_dir: Path) -> None:
        """Export DataFrames, CSV files, and plots after simulation."""
        output_dir.mkdir(parents=True, exist_ok=True)

        if not self.populationhistory:
            raise ValueError("No population statistics were collected")

        population_df = pd.DataFrame(self.populationhistory)
        events_df = pd.DataFrame(
            self.events,
            columns=["turn", "event", "description"],
        )

        if not events_df.empty:
            events_df = events_df.sort_values(
                "turn", kind="stable"
            ).reset_index(drop=True)

        self._save_population(population_df, output_dir)
        self._save_reproduction(
            population_df, events_df, output_dir
        )
        self._save_timeline(events_df, output_dir)

    def _save_population(
            self, df: pd.DataFrame, output_dir: Path
    ) -> None:
        """Export living-organism statistics and a line plot."""
        df.to_csv(output_dir / "population.csv", index=False)

        ax = df.plot(
            x="turn",
            y=list(self.organismtypes),
            figsize=(11, 6),
            title="Living Organisms Over Time",
        )

        ax.set_xlabel("Simulation Turn")
        ax.set_ylabel("Number Alive")
        ax.grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_dir / "population.png", dpi=150)
        plt.close()

    def _save_reproduction(
            self,
            population_df: pd.DataFrame,
            events_df: pd.DataFrame,
            output_dir: Path,
    ) -> None:
        """Export births per turn and cumulative reproduction."""
        reproduction_events = events_df[
            events_df["event"] == "Reproduction"
            ]

        birthsperturn = (
            reproduction_events.groupby("turn")
            .size()
            .rename("births")
        )

        reproduction_df = pd.DataFrame({
            "turn": population_df["turn"]
        })

        reproduction_df["births"] = (
            reproduction_df["turn"]
            .map(birthsperturn)
            .fillna(0)
            .astype(int)
        )

        reproduction_df["cumulative_births"] = (
            reproduction_df["births"].cumsum()
        )

        reproduction_df.to_csv(
            output_dir / "reproductions.csv",
            index=False,
        )

        ax = reproduction_df.plot(
            x="turn",
            y=["births", "cumulative_births"],
            figsize=(11, 6),
            title="Herbivore Reproductions Over Time",
        )

        ax.set_xlabel("Simulation Turn")
        ax.set_ylabel("Number of Births")
        ax.grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_dir / "reproductions.png", dpi=150)
        plt.close()

    def _save_timeline(
            self, df: pd.DataFrame, output_dir: Path
    ) -> None:
        """Export event history and a visual event timeline."""
        df.to_csv(output_dir / "timeline.csv", index=False)

        event_types = (
            "Reproduction",
            "Consumption",
            "Extinction",
        )

        fig, ax = plt.subplots(figsize=(12, 5))

        for event_type in event_types:
            subset = df[df["event"] == event_type]
            counts = subset.groupby("turn").size()

            if not counts.empty:
                ax.scatter(
                    counts.index,
                    [event_type] * len(counts),
                    s=25 + counts.to_numpy() * 12,
                    alpha=0.65,
                    label=event_type,
                )

        ax.set_title("Simulation Event Timeline")
        ax.set_xlabel("Simulation Turn")
        ax.set_ylabel("Event Type")
        ax.grid(axis="x", alpha=0.3)

        plt.tight_layout()
        fig.savefig(output_dir / "timeline.png", dpi=150)
        plt.close(fig)
