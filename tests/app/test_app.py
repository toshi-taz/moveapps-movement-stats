import unittest
import movingpandas as mpd
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from datetime import datetime, timezone
from unittest.mock import MagicMock
from app.app import App


class TestApp(unittest.TestCase):

    def _make_io_mock(self):
        mock_io = MagicMock()
        mock_io.create_artifacts_file.side_effect = lambda name: f"/tmp/{name}"
        return mock_io

    def _make_collection(self):
        data = {
            "geometry": [Point(0,0), Point(1,1), Point(2,2),
                         Point(3,3), Point(4,4), Point(5,5)],
            "individual_id": ["A","A","A","B","B","B"],
        }
        t = [datetime(2024,1,1,i, tzinfo=timezone.utc) for i in range(3)] + \
            [datetime(2024,1,2,i, tzinfo=timezone.utc) for i in range(3)]
        gdf = gpd.GeoDataFrame(data, index=pd.DatetimeIndex(t), crs="EPSG:4326")
        return mpd.TrajectoryCollection(gdf, traj_id_col="individual_id")

    def test_returns_trajectory_collection(self):
        result = App(self._make_io_mock()).execute(self._make_collection(), {})
        self.assertIsInstance(result, mpd.TrajectoryCollection)

    def test_csv_artifact_created(self):
        mock_io = self._make_io_mock()
        App(mock_io).execute(self._make_collection(), {})
        calls = [c[0][0] for c in mock_io.create_artifacts_file.call_args_list]
        self.assertIn("movement_stats.csv", calls)

    def test_plot_artifact_created(self):
        mock_io = self._make_io_mock()
        App(mock_io).execute(self._make_collection(), {})
        calls = [c[0][0] for c in mock_io.create_artifacts_file.call_args_list]
        self.assertIn("distance_plot.png", calls)

    def test_output_same_as_input(self):
        tc = self._make_collection()
        result = App(self._make_io_mock()).execute(tc, {})
        self.assertEqual(len(result.trajectories), len(tc.trajectories))


if __name__ == "__main__":
    unittest.main()
