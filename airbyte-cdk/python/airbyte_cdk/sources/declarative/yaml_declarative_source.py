#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

import pkgutil

from airbyte_cdk.sources.declarative.manifest_declarative_source import ManifestDeclarativeSource
from airbyte_cdk.sources.declarative.parsers.yaml_parser import YamlParser
from airbyte_cdk.sources.declarative.types import ConnectionDefinition


class YamlDeclarativeSource(ManifestDeclarativeSource):
    """Declarative source defined by a yaml file"""

    def __init__(self, path_to_yaml):
        """
        :param path_to_yaml: Path to the yaml file describing the source
        """
        self._path_to_yaml = path_to_yaml
        source_config = self._read_and_parse_yaml_file(path_to_yaml)
        super().__init__(source_config)

    def _read_and_parse_yaml_file(self, path_to_yaml_file) -> ConnectionDefinition:
        package = self.__class__.__module__.split(".")[0]

        yaml_config = pkgutil.get_data(package, path_to_yaml_file)
        decoded_yaml = yaml_config.decode()
        return YamlParser().parse(decoded_yaml)

    def _emit_manifest_debug_message(self, extra_args: dict):
        extra_args["path_to_yaml"] = self._path_to_yaml
        self.logger.debug("declarative source created from parsed YAML manifest", extra=extra_args)
