from .histdata.api import download_hist_data
from .histdata.domain import Platform, TimeFrame
from pathlib import Path
import typer
from typer import Argument, Option, colors, secho


PARENT_DIR = Path(__file__).parent.parent


def download_all(
        pair: str=Argument(..., help='Forex market to download data of e.g. eurusd'), 
        fromyear: int=Argument(..., help='Starting year of the data to download e.g. 2024'),
        timeframe: TimeFrame=Option(TimeFrame.TICK_DATA, '-t', help='Typology of the data'),
        plarform: Platform=Option(Platform.GENERIC_ASCII, '-p', help='Platform relating to the data format')
    ):
    outDir: Path=PARENT_DIR / f'output_{pair.upper()}'
    secho(f'{pair.upper()} download since {fromyear}...', fg=colors.MAGENTA)
    
    # Setup folders
    outDir.mkdir(exist_ok=True)
    outDir = outDir / plarform
    outDir.mkdir(exist_ok=True)

    # Gather common parameters for the iterative steps
    COMMON_KWARGS  = {
        'pair': pair,
        'platform': plarform,
        'time_frame': timeframe,
        'output_directory': str(outDir.relative_to(PARENT_DIR)),
        'verbose': False
    }

    try:
        year = fromyear
        while True:
            secho(f'Will attempt to dowload yearly data for {year}...', fg=colors.CYAN)
            could_download_full_year = False
            try:
                # DOWLOAD YEAR PER YEAR
                print('-', download_hist_data(year=str(year), **COMMON_KWARGS))
                could_download_full_year = True
            except AssertionError as aerr:
                secho(f'Error dowloading year by year data because:', fg=colors.YELLOW)
                secho(f'[{aerr}]', fg=colors.WHITE)
                secho(f'Will attempt to dowload monthly data...', fg=colors.CYAN)
                pass  # lets download it month by month.

            month = 1
            while not could_download_full_year and month <= 12:
                # DOWLOAD MONTH PER MONTH FOR REMAINING YEAR
                print('-', download_hist_data(year=str(year), month=str(month), **COMMON_KWARGS))
                month += 1
                pass

            year += 1
    except Exception as err:
        secho(f'Exiting program because either all has been downloaded or:', fg=colors.YELLOW)
        secho(f'[{err}]', fg=colors.WHITE)
        secho(f'[DONE] for currency pair {pair.upper()}', fg=colors.MAGENTA)
        pass


if __name__ == '__main__':
    typer.run(download_all)
