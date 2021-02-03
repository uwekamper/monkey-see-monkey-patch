import os
import click
import itertools
from werkzeug.serving import WSGIRequestHandler

from lektor.devserver import process_extra_flags
from lektor.devserver BackgroundBuilder
from lektor.devserver WebAdmin
from lektor.devserver run_simple
from lektor.devserver browse_to_address
from lektor.devserver SilentWSGIRequestHandler
from lektor.cli import pass_context
from lektor.cli import buildflag
from lektor.cli import extraflag
from lektor.cli import pruneflag

def run_server(
    bindaddr,
    env,
    output_path,
    prune=True,
    verbosity=0,
    lektor_dev=False,
    ui_lang="en",
    browse=False,
    extra_flags=None,
):
    """This runs a server but also spawns a background process.  It's
    not safe to call this more than once per python process!
    """
    wz_as_main = os.environ.get("WERKZEUG_RUN_MAIN") == "true"
    in_main_process = not lektor_dev or wz_as_main
    extra_flags = process_extra_flags(extra_flags)

    if in_main_process:
        background_builder = BackgroundBuilder(
            env,
            output_path=output_path,
            prune=prune,
            verbosity=verbosity,
            extra_flags=extra_flags,
        )
        background_builder.setDaemon(True)
        background_builder.start()
        env.plugin_controller.emit(
            "server-spawn", bindaddr=bindaddr, extra_flags=extra_flags
        )

    app = WebAdmin(
        env,
        output_path=output_path,
        verbosity=verbosity,
        debug=lektor_dev,
        ui_lang=ui_lang,
        extra_flags=extra_flags,
    )
    
    app.register_blueprint(env.plugins['facebook'].get_blueprint())

    dt = None
    if lektor_dev and not wz_as_main:
        dt = DevTools(env)
        dt.start()

    if browse:
        browse_to_address(bindaddr)

    try:
        return run_simple(
            bindaddr[0],
            bindaddr[1],
            app,
            use_debugger=True,
            threaded=True,
            use_reloader=lektor_dev,
            request_handler=not lektor_dev
            and SilentWSGIRequestHandler
            or WSGIRequestHandler,
        )
    finally:
        if dt is not None:
            dt.stop()
        if in_main_process:
            env.plugin_controller.emit("server-stop")


@click.group()
def cli():
    pass


@cli.command('server', short_help='Launch a local server.')
@click.option('-h', '--host', default='127.0.0.1',
              help='The network interface to bind to.  The default is the '
              'loopback device, but by setting it to 0.0.0.0 it becomes '
              'available on all network interfaces.')
@click.option('-p', '--port', default=5000, help='The port to bind to.',
              show_default=True)
@click.option('-O', '--output-path', type=click.Path(), default=None,
              help='The dev server will build into the same folder as '
              'the build command by default.')
@pruneflag
@click.option('-v', '--verbose', 'verbosity', count=True,
              help='Increases the verbosity of the logging.')
@extraflag
@buildflag
@click.option('--browse', is_flag=True)
@pass_context
def server_cmd(ctx, host, port, output_path, prune, verbosity,
               extra_flags, build_flags, browse):
    """The server command will launch a local server for development.

    Lektor's development server will automatically build all files into
    pages similar to how the build command with the `--watch` switch
    works, but also at the same time serve up the website on a local
    HTTP server.
    """
    extra_flags = tuple(itertools.chain(extra_flags or (), build_flags or ()))
    if output_path is None:
        output_path = ctx.get_default_output_path()
    ctx.load_plugins(extra_flags=extra_flags)
    click.echo(' * Project path: %s' % ctx.get_project().project_path)
    click.echo(' * Output path: %s' % output_path)
    run_server((host, port), env=ctx.get_env(), output_path=output_path,
               prune=prune, verbosity=verbosity, ui_lang=ctx.ui_lang,
               extra_flags=extra_flags,
               lektor_dev=os.environ.get('LEKTOR_DEV') == '1',
               browse=browse)


if __name__ == "__main__":
    cli()