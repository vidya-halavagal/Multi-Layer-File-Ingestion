from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType


def create_spark_session(app_name: str, master: str = "local[*]") -> SparkSession:
    """Create a Spark session, or reuse one that is already running.

    Args:
        app_name: Name shown for this application in Spark.
        master: Where Spark runs. Defaults to local, using all CPU cores.

    Returns:
        The active SparkSession.
    """
    return SparkSession.builder.appName(app_name).master(master).getOrCreate()


def read_file_to_dataframe(
    spark: SparkSession,
    file_path: str,
    schema: StructType,
    delimiter: str = ",",
    header: bool = True,
    mode: str = "FAILFAST",
) -> DataFrame:
    """Read a delimited text file into a Spark DataFrame.

    Args:
        spark: Active Spark session.
        file_path: Full path of the file to read.
        schema: Column names and types the DataFrame must follow.
        delimiter: Character that separates the columns. Defaults to a comma.
        header: True if the first line is a header row, so Spark skips it.
        mode: How to handle bad values. Defaults to FAILFAST, which raises
            an error instead of silently turning a bad value into null.

    Returns:
        A DataFrame with one row per data line. Column names come from the schema.
    """
    return (
        spark.read.options(header=header, sep=delimiter, mode=mode)
        .schema(schema)
        .csv(file_path)
    )
