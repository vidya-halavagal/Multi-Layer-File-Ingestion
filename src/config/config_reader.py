"""Configuration reader: loads the YAML settings and builds the Spark schema."""

from pathlib import Path
from typing import Any

import yaml
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

# --- Constants ---

# Map the data type names used in YAML to their PySpark equivalents.
TYPE_MAP = {
    "string": StringType(),
    "integer": IntegerType(),
    "double": DoubleType(),
}

# Data type names accepted in the YAML configuration.
SUPPORTED_TYPES = frozenset(TYPE_MAP)


# --- Load ---

def load_yaml_config(yaml_file: str | Path) -> dict[str, Any]:
    """
    Load configuration settings from a YAML file.

    Args:
        yaml_file: Path to the YAML configuration file.

    Returns:
        The configuration loaded from the YAML file.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the YAML syntax is invalid or the file is empty.
        TypeError: If the YAML root is not a dictionary.
    """
    config_path = Path(yaml_file)

    # Stop early if the configuration file is missing.
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file does not exist: {config_path}")

    # Open the file and safely parse its YAML content.
    try:
        with config_path.open("r", encoding="utf-8") as file:
            settings = yaml.safe_load(file)
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid YAML configuration syntax: {error}") from error

    # Ensure the YAML is not empty.
    if settings is None:
        raise ValueError("YAML configuration must not be empty")

    # Ensure the YAML root is a dictionary of settings.
    if not isinstance(settings, dict):
        raise TypeError("YAML configuration must contain a dictionary at its root")

    return settings


# --- Validate ---

def validate_file_columns(file_columns: dict[str, str]) -> dict[str, str]:
    """
    Validate and normalize expected file column names and data types.

    Args:
        file_columns: Dictionary mapping column names to type names.

    Returns:
        A new dictionary with trimmed column names and normalized data types.

    Raises:
        TypeError: If the input is not a dictionary, or a key/value is not a string.
        ValueError: If the dictionary is empty, a name/type is empty, a normalized
            column name is duplicated, or a data type is unsupported.
    """
    # Confirm that the supplied configuration has the expected structure.
    if not isinstance(file_columns, dict):
        raise TypeError("file_columns must be a dictionary")

    if not file_columns:
        raise ValueError("file_columns must not be empty")

    validated_columns = {}

    # Validate and normalize each column definition.
    for column_name, type_name in file_columns.items():
        # String methods are only safe after checking both values.
        if not isinstance(column_name, str) or not isinstance(type_name, str):
            raise TypeError("Column names and data types must be strings")

        clean_name = column_name.strip()
        clean_type = type_name.strip().lower()

        if not clean_name:
            raise ValueError("Column name cannot be empty")

        if not clean_type:
            raise ValueError(
                f"Data type cannot be empty for column {column_name!r}"
            )

        # Prevent names such as "id" and " id " becoming duplicate columns.
        if clean_name in validated_columns:
            raise ValueError(
                f"Duplicate column name after trimming: {clean_name!r}"
            )

        if clean_type not in SUPPORTED_TYPES:
            raise ValueError(
                f"Unsupported data type {clean_type!r} for column {clean_name!r}. "
                f"Supported types: {sorted(SUPPORTED_TYPES)}"
            )

        validated_columns[clean_name] = clean_type

    return validated_columns


# --- Get ---

def get_file_columns(config: dict[str, Any]) -> dict[str, str]:
    """
    Extract and validate file columns from the loaded configuration.

    Args:
        config: Configuration dictionary loaded from YAML.

    Returns:
        Validated file column names and data types.

    Raises:
        KeyError: If the required configuration section or key is missing.
        TypeError or ValueError: If the column configuration is invalid.
    """
    try:
        file_columns = config["file_validation"]["file_columns"]
    except KeyError as error:
        raise KeyError(f"Missing configuration key: {error}") from error

    # Keep all column validation rules in the reusable validator.
    return validate_file_columns(file_columns)


def get_expected_columns(config: dict[str, Any]) -> list[str]:
    """
    Extract the expected column names, in file order.

    Args:
        config: Configuration dictionary loaded from YAML.

    Returns:
        List of expected column names.
    """
    file_columns = get_file_columns(config)

    return list(file_columns)


def get_file_name_pattern(config: dict[str, Any]) -> str:
    """
    Extract the file name pattern from the loaded configuration.

    Args:
        config: Configuration dictionary loaded from YAML.

    Returns:
        Regular expression used to validate incoming file names.

    Raises:
        KeyError: If the required configuration section or key is missing.
    """
    try:
        return config["file_validation"]["file_name_pattern"]
    except KeyError as error:
        raise KeyError(f"Missing configuration key: {error}") from error


# --- Build ---

def build_spark_schema(file_columns: dict[str, str]) -> StructType:
    """
    Build a PySpark schema from validated file column definitions.

    Args:
        file_columns: Validated dictionary mapping column names to type names.

    Returns:
        A PySpark StructType containing the configured fields.
    """
    fields = []

    # Convert each configured data type into a Spark StructField.
    for column_name, type_name in file_columns.items():
        spark_type = TYPE_MAP[type_name]
        fields.append(StructField(column_name, spark_type, nullable=True))

    # StructType represents the complete schema; StructField represents one column.
    return StructType(fields)
