from .histdata.api import download_hist_data, Platform, TimeFrame
from pathlib import Path


PARENT_DIR = Path(__file__).parent.parent


def download_all(
        pair='eurusd', 
        fromYear=2024,
        plarform=Platform.GENERIC_ASCII,
        timeframe=TimeFrame.TICK_DATA
    ):
    outDir: Path=PARENT_DIR / f'output_{pair.upper()}'
    print(f'{pair.upper()} download since {fromYear}...')
    
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
        year = fromYear
        while True:
            could_download_full_year = False
            try:
                # DOWLOAD YEAR PER YEAR
                print('-', download_hist_data(year=str(year), **COMMON_KWARGS))
                could_download_full_year = True
            except AssertionError as aerr:
                print(f'Error dowloading year by year data because\n[{aerr}]')
                print(f'Will attempt to dowload month by month data...')
                pass  # lets download it month by month.

            month = 1
            while not could_download_full_year and month <= 12:
                # DOWLOAD MONTH PER MONTH FOR REMAINING YEAR
                print('-', download_hist_data(year=str(year), month=str(month), **COMMON_KWARGS))
                month += 1
                pass

            year += 1
    except Exception as err:
        print(f'Exiting program due to:\n[{err}]')
        print(f'[DONE] for currency {pair.upper()}')
        pass


if __name__ == '__main__':
    download_all()
