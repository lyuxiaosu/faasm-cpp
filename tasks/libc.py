from subprocess import run

from os.path import join

from invoke import task

from faasmtools.env import (
    PROJ_ROOT,
    USABLE_CPUS,
)

from faasmtools.build import (
    WASM_CC,
    WASM_AR,
    WASM_NM,
    WASM_SYSROOT,
)


@task(default=True)
def build(ctx, clean=False):
    """
    Builds the wasi libc fork in this directory
    """
    libc_dir = join(PROJ_ROOT, "third-party", "wasi-libc")

    if clean:
        run("make clean", shell=True, check=True, cwd=libc_dir)

    make_cmd = [
        "make",
        "-j {}".format(USABLE_CPUS),
        "THREAD_MODEL=faasm",
        "WASM_CC={}".format(WASM_CC),
        "WASM_AR={}".format(WASM_AR),
        "WASM_NM={}".format(WASM_NM),
        "SYSROOT={}".format(WASM_SYSROOT),
    ]
    make_cmd = " ".join(make_cmd)
    print(make_cmd)

    # Push tag
    run(make_cmd, check=True, shell=True, cwd=libc_dir)
