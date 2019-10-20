import os
import shutil

from .cli import HasCLI
from dbt.contracts.rpc import (
    RPCNoParameters, RemoteEmptyResult, RemoteMethodFlags,
)
from dbt.task.deps import DepsTask


def _clean_deps(config):
    modules_dir = os.path.join(config.project_root, config.modules_path)
    shutil.rmtree(modules_dir)
    os.makedirs(modules_dir)


class RemoteDepsTask(HasCLI[RPCNoParameters, RemoteEmptyResult], DepsTask):
    METHOD_NAME = 'deps'

    def get_flags(self) -> RemoteMethodFlags:
        return (
            RemoteMethodFlags.RequiresConfigReloadBefore |
            RemoteMethodFlags.RequiresManifestReloadAfter
        )

    def set_args(self, params: RPCNoParameters):
        pass

    def handle_request(self) -> RemoteEmptyResult:
        _clean_deps(self.config)
        self.run()
        return RemoteEmptyResult([])
