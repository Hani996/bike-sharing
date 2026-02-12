"""
Data analysis engine for the CityBike platform.

Contains the BikeShareSystem class that orchestrates:
    - CSV loading and cleaning
    - Answering business questions using Pandas
    - Generating summary reports

Students should implement the cleaning logic and at least 10 analytics methods.
"""

import pandas as pd
import numpy as np
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


class BikeShareSystem:
    """Central analysis class — loads, cleans, and analyzes bike-share data.

    Attributes:
        trips: DataFrame of trip records.
        stations: DataFrame of station metadata.
        maintenance: DataFrame of maintenance records.
    """

    def __init__(self) -> None:
        self.trips: pd.DataFrame | None = None
        self.stations: pd.DataFrame | None = None
        self.maintenance: pd.DataFrame | None = None

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_data(self) -> None:
        """Load raw CSV files into DataFrames."""
        self.trips = pd.read_csv(DATA_DIR / "trips.csv")
        self.stations = pd.read_csv(DATA_DIR / "stations.csv")
        self.maintenance = pd.read_csv(DATA_DIR / "maintenance.csv")

        print(f"Loaded trips: {self.trips.shape}")
        print(f"Loaded stations: {self.stations.shape}")
        print(f"Loaded maintenance: {self.maintenance.shape}")

    # ------------------------------------------------------------------
    # Data inspection (provided)
    # ------------------------------------------------------------------

    def inspect_data(self) -> None:
        """Print basic info about each DataFrame."""
        for name, df in [
            ("Trips", self.trips),
            ("Stations", self.stations),
            ("Maintenance", self.maintenance),
        ]:
            print(f"\n{'='*40}")
            print(f"  {name}")
            print(f"{'='*40}")
            print(df.info())
            print(f"\nMissing values:\n{df.isnull().sum()}")
            print(f"\nFirst 3 rows:\n{df.head(3)}")

    # ------------------------------------------------------------------
    # Data cleaning
    # ------------------------------------------------------------------

    def clean_data(self) -> None:
        """Clean all DataFrames and export to CSV.

        Steps to implement:
            1. Remove duplicate rows
            2. Parse date/datetime columns
            3. Convert numeric columns stored as strings
            4. Handle missing values (document your strategy!)
            5. Remove invalid entries (e.g. end_time < start_time)
            6. Standardize categorical values
            7. Export cleaned data to data/trips_clean.csv etc.

        TODO: implement each step below.
        """
        if self.trips is None:
            raise RuntimeError("Call load_data() first")

        # --- Step 1: Remove duplicates ---
        self.trips = self.trips.drop_duplicates(subset=["trip_id"])
        print(f"After dedup: {self.trips.shape[0]} trips")

        # --- Step 2: Parse dates ---
        # TODO: convert start_time, end_time to datetime
        self.trips["start_time"] = pd.to_datetime(self.trips["start_time"])
        self.trips["end_time"] = pd.to_datetime(self.trips["end_time"])

        # --- Step 3: Convert numeric columns ---
        # TODO: ensure duration_minutes and distance_km are float
        self.trips["duration_minutes"]=pd.to_numeric(self.trips["duration_minutes"])
        self.trips["distance_km"]=pd.to_numeric(self.trips["distance_km"])

        

        # --- Step 4: Handle missing values ---
        # TODO: decide on a strategy and document it
        # Example: self.trips["duration_minutes"].fillna(..., inplace=True)
        # self.trips["duration_minutes"].fillna(..., inplace=True)
        # Missing values strategy:
        # - Trips with missing duration_minutes, distance_km, start_time, or end_time
        #   are removed because they cannot be used in time or distance-based analysis.
        # - Missing status values are filled with 'unknown'.
        # - Maintenance records with missing cost are dropped.
        self.trips = self.trips.dropna(subset=['duration_minutes', 'distance_km','start_time','end_time'])
         
        

        # --- Step 5: Remove invalid entries ---
        # TODO: drop rows where end_time < start_time
        self.trips=self.trips[self.trips['end_time'] >= self.trips['start_time']]
        

        # --- Step 6: Standardize categoricals ---
        # TODO: e.g. self.trips["status"].str.lower().str.strip()
        self.trips["user_type"]=self.trips["user_type"].str.lower().str.strip()
        
    

        # --- Step 7: Export cleaned datasets ---

        self.trips.info()
        self.stations.info()
        self.maintenance.info()
        # print("Missing values in trips:")
        # print(self.trips.isna().sum())
        # print("Missing values in stations:")
        # print(self.stations.isna().sum())
        # print("Missing values in maintenance:")
        # print(self.maintenance.isna().sum())
        #fill status in trips with 'unknown'
        self.trips['status']=self.trips['status'].fillna('unknown')
        #dropp missing vaölue in maintenance in cost column
        self.maintenance=self.maintenance.dropna(subset=['cost'])
        
        print(self.trips.isna().sum())
        print(self.maintenance.isna().sum())
        
        self.trips.to_csv(DATA_DIR / "trips_clean.csv", index=False)
        self.stations.to_csv(DATA_DIR / "stations_clean.csv", index=False)
        self.maintenance.to_csv(DATA_DIR / "maintenance_clean.csv", index=False)

        
        

        print("Cleaning complete.")

    # ------------------------------------------------------------------
    # Analytics — Business Questions
    # ------------------------------------------------------------------

    def total_trips_summary(self) -> dict:
        """Q1: Total trips, total distance, average duration.

        Returns:
            Dict with 'total_trips', 'total_distance_km', 'avg_duration_min'.
        """
        df = self.trips
        return {
            "total_trips": len(df),
            "total_distance_km": round(df["distance_km"].sum(), 2),
            "avg_duration_min": round(df["duration_minutes"].mean(), 2),
        }

    def top_start_stations(self, n: int = 10) -> pd.DataFrame:
        """Q2: Top *n* most popular start stations.
        
        

        TODO: use value_counts() or groupby on start_station_id,
              merge with station names.
              
        """
        
        # Get value counts for start_station_id and convert to DataFrame
        counts = self.trips["start_station_id"].value_counts().head(n).reset_index()
        counts.columns = ["start_station_id", "trip_count"]

        
        # Merge with station names
        result = counts.merge(
            self.stations[["station_id", "station_name"]], 
            left_on="start_station_id", 
            right_on="station_id",
            how="left"
        )
        
        return result[["station_name", "trip_count"]]
        

    def peak_usage_hours(self) -> pd.Series:
        """Q3: Trip count by hour of day.

        TODO: extract hour from start_time and count trips per hour.
        """
        # self.trips["hour"]=self.trips["start_time"].dt.hour
        # return self.trips["hour"].value_counts().sort_index()
        df = self.trips.copy()
        df["hour"] = df["start_time"].dt.hour
        return df["hour"].value_counts().sort_index()
    
        
        # raise NotImplementedError("peak_usage_hours")

    def busiest_day_of_week(self) -> pd.Series:
        """Q4: Trip count by day of week.

        TODO: extract day-of-week from start_time, count.
        """
        self.trips["start_time"] = pd.to_datetime(self.trips["start_time"])
        self.trips["day"]=self.trips["start_time"].dt.day_name()
        return self.trips["day"].value_counts().sort_index()
    
        
        # print(self.trips["start_time"].dtype)
        
        # raise NotImplementedError("busiest_day_of_week")

    def avg_distance_by_user_type(self) -> pd.Series:
        """Q5: Average trip distance grouped by user type."""
        return self.trips.groupby("user_type")["distance_km"].mean().round(2)
        # raise NotImplementedError("avg_distance_by_user_type")

    def monthly_trip_trend(self) -> pd.Series:
        """Q7: Monthly trip counts over time.

        TODO: extract year-month from start_time, group, count.
        """
        self.trips["year_month"]=self.trips["start_time"].dt.to_period("M")
        return self.trips["year_month"].value_counts().sort_index()
        # raise NotImplementedError("monthly_trip_trend")

    def top_active_users(self, n: int = 15) -> pd.DataFrame:
        """Q8: Top *n* most active users by trip count.

        TODO: group by user_id, count trips, sort descending.
        """
        counts = self.trips["user_id"].value_counts().head(n)
        return counts.to_frame().reset_index().rename(columns={"user_id": "user_id", 0: "trip_count"})
        # raise NotImplementedError("top_active_users")

    def maintenance_cost_by_bike_type(self) -> pd.Series:
        """Q9: Total maintenance cost per bike type.

        TODO: group maintenance by bike_type, sum cost.
        """
        return self.maintenance.groupby("bike_type")["cost"].sum().round(2)
        # raise NotImplementedError("maintenance_cost_by_bike_type")

    def top_routes(self, n: int = 10) -> pd.DataFrame:
        """Q10: Most common start→end station pairs.
        

        TODO: group by (start_station_id, end_station_id), count, sort.
        """
        route_counts = self.trips.groupby(["start_station_id", "end_station_id"]).size()
        top_routes = route_counts.nlargest(n)
        top_routes_df = top_routes.reset_index(name="trip_count")
        # Merge with station names for start and end stations
        start_stations = self.stations[["station_id", "station_name"]].rename(columns={"station_id": "start_station_id", "station_name": "start_station_name"})
        end_stations = self.stations[["station_id", "station_name"]].rename(columns={"station_id": "end_station_id", "station_name": "end_station_name"})
        result = top_routes_df.merge(start_stations, on="start_station_id", how="left")
        result = result.merge(end_stations, on="end_station_id", how="left")
        return result[["start_station_name", "end_station_name", "trip_count"]]
    # ------------------------------------------------------------------
    # Add more analytics methods here (Q6, Q11–Q14)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def generate_summary_report(self) -> None:
        """Write a summary text report to output/summary_report.txt.

        TODO:
            - Uncomment and complete each section below
            - Add results from remaining analytics methods
        """
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / "summary_report.txt"

        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("  CityBike — Summary Report")
        lines.append("=" * 60)

        # --- Q1: Overall summary ---
        summary = self.total_trips_summary()
        lines.append("\n--- Overall Summary ---")
        lines.append(f"  Total trips       : {summary['total_trips']}")
        lines.append(f"  Total distance    : {summary['total_distance_km']} km")
        lines.append(f"  Avg duration      : {summary['avg_duration_min']} min")

        # --- Q2: Top start stations ---
        # TODO: uncomment once top_start_stations() is implemented
        top_stations = self.top_start_stations()
        lines.append("\n--- Top 10 Start Stations ---")
        lines.append(top_stations.to_string(index=False))

        # --- Q3: Peak usage hours ---
        # TODO: uncomment once peak_usage_hours() is implemented
        hours = self.peak_usage_hours()
        lines.append("\n--- Peak Usage Hours ---")
        lines.append(hours.to_string())
        # --- Q4: Busiest days of week ---
        days = self.busiest_day_of_week()
        lines.append("\n--- Busiest Days of Week ---")
        lines.append(days.to_string())
        
        # --- Q5: Average distance by user type ---
        avg_dist = self.avg_distance_by_user_type()
        lines.append("\n--- Avg Distance by User Type ---")
        lines.append(avg_dist.to_string())

        # --- Q9: Maintenance cost by bike type ---
        # TODO: uncomment once maintenance_cost_by_bike_type() is implemented
        maint_cost = self.maintenance_cost_by_bike_type()
        lines.append("\n--- Maintenance Cost by Bike Type ---")
        lines.append(maint_cost.to_string())

        # TODO: add more sections for Q4–Q8, Q10–Q14 …

        report_text = "\n".join(lines) + "\n"
        report_path.write_text(report_text)
        print(f"Report saved to {report_path}")
