from cx_Freeze import setup, Executable

icon_file = "database"
buildOptions = dict(icon = icon_file)

setup(
    name = "gen_data_Oracle",
    version = "0.3",
    description = "Generator Data Oracle",
    options = dict(build_exe = buildOptions),
    executables = [Executable("gen_data_Oracle.py")]
)