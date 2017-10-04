from alpha_vantage.sectorperformance import SectorPerformances

sp = SectorPerformances(key='GSD3E3P11LSBZG5O', output_format='pandas')
data, meta_data = sp.get_sector()

print(data.head())
