import os,datetime, arcpy, time

INPUT_STRING=r'''1 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,1000,1 1000,2000,2 2000,5000,3
2 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,2,1 2,5,3 5,6,4
3 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,1000,1 1000,2000,2 2000,5000,3
4 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,2,1 2,5,3 5,6,4
5 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,1000,1 1000,2000,2 2000,5000,3
6 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,2,1 2,5,3 5,6,4
7 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,1000,1 1000,2000,2 2000,5000,3
8 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,2,1 2,5,3 5,6,4
9 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,1000,1 1000,2000,2 2000,5000,3
10 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,2,1 2,5,3 5,6,4
11 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,1000,1 1000,2000,2 2000,5000,3
12 1.0 Q:\CHII\0_GIS\CHII_Exports\TEST_LH_DEMB_m534_1m.tif 0,2,1 2,5,3 5,6,4'''

VAT_TEMPLATE = '''<RasterFunctionTemplate xsi:type='typens:RasterFunctionTemplate' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xs='http://www.w3.org/2001/XMLSchema' xmlns:typens='http://www.esri.com/schemas/ArcGIS/10.5'>
	<Name>VATtest</Name>
	<Description>A raster function template.</Description>
	<Function xsi:type='typens:BandArithmeticFunction'>
		<Name>Band Arithmetic Function</Name>
		<Description>Calculates indexes using the inbuilt formulae or user-defined expression.</Description>
		<PixelType>U8</PixelType>
	</Function>
	<Arguments xsi:type='typens:BandArithmeticFunctionArguments'>
		<Names xsi:type='typens:ArrayOfString'>
			<String>Raster</String>
			<String>BandIndexes</String>
			<String>Method</String>
		</Names>
		<Values xsi:type='typens:ArrayOfAnyType'>
			<AnyType xsi:type='typens:RasterFunctionTemplate'>
				<Name>Raster Function Template</Name>
				<Description>A raster function template.</Description>
				<Function xsi:type='typens:CompositeBandFunction'>
					<Name>Composite Band Function</Name>
					<Description>Combines rasters to form a multiband raster.</Description>
					<PixelType>U8</PixelType>
				</Function>
				<Arguments xsi:type='typens:RasterFunctionVariable'>
					<Name>Rasters_2018226_215812_169</Name>
					<Description/>
					<Value xsi:type='typens:ArrayOfArgument'>{0}
					</Value>
					<IsDataset>false</IsDataset>
				</Arguments>
				<Help/>
				<Type>0</Type>
				<Thumbnail/>
				<Definition/>
				<Group/>
				<Tag/>
				<ThumbnailEx/>
			</AnyType>
			<AnyType xsi:type='typens:RasterFunctionVariable'>
				<Name>BandIndexes_2018226_215812_169</Name>
				<Description/>
				<Value xsi:type='xs:string'>{1}</Value>
				<IsDataset>false</IsDataset>
			</AnyType>
			<AnyType xsi:type='typens:RasterFunctionVariable'>
				<Name>Method_2018226_215812_169</Name>
				<Description/>
				<Value xsi:type='xs:int'>0</Value>
				<IsDataset>false</IsDataset>
			</AnyType>
		</Values>
	</Arguments>
	<Help/>
	<Type>0</Type>
	<Thumbnail/>
	<Definition/>
	<Group/>
	<Tag/>
	<ThumbnailEx/>
</RasterFunctionTemplate>'''

RASTER_TEMPLATE = '''\n						<Argument xsi:type='typens:RasterFunctionTemplate'>
							<Name>Raster Function Template</Name>
							<Description>A raster function template.</Description>
							<Function xsi:type='typens:RemapFunction'>
								<Name>Remap Function</Name>
								<Description>Remaps pixel values using user-defined pixel ranges or an external table.</Description>
								<PixelType>U8</PixelType>
							</Function>
							<Arguments xsi:type='typens:RemapFunctionArguments'>
								<Names xsi:type='typens:ArrayOfString'>
									<String>Raster</String>
									<String>InputRanges</String>
									<String>OutputValues</String>
									<String>NoDataRanges</String>
									<String>AllowUnmatched</String>
								</Names>
								<Values xsi:type='typens:ArrayOfAnyType'>
									<AnyType xsi:type='typens:RasterFunctionVariable'>
										<Name>{NAME}</Name>
										<Description/>
										<Value xsi:type='typens:RasterDatasetName'>
											<WorkspaceName xsi:type='typens:WorkspaceName'>
												<NameString>Raster Workspace = {PATH}\;</NameString>
												<PathName>{PATH}\</PathName>
												<BrowseName>Raster Data</BrowseName>
												<WorkspaceFactoryProgID>esriDataSourcesRaster.RasterWorkspaceFactory.1</WorkspaceFactoryProgID>
												<WorkspaceType>esriFileSystemWorkspace</WorkspaceType>
												<ConnectionProperties xsi:type='typens:PropertySet'>
													<PropertyArray xsi:type='typens:ArrayOfPropertySetProperty'>
														<PropertySetProperty xsi:type='typens:PropertySetProperty'>
															<Key>DATABASE</Key>
															<Value xsi:type='xs:string'>{PATH}\</Value>
														</PropertySetProperty>
													</PropertyArray>
												</ConnectionProperties>
											</WorkspaceName>
											<Name>{FILE}</Name>
											<NameString>RASTER: Workspace = {PATH}\; RasterDataset = {FILE};</NameString>
											<Category>Raster Dataset</Category>
										</Value>
										<IsDataset>true</IsDataset>
									</AnyType>
									<AnyType xsi:type='typens:RasterFunctionVariable'>
										<Name>InputRanges_2018226_215812_169</Name>
										<Description/>
										<Value xsi:type='typens:ArrayOfDouble'>{BREAKS}
										</Value>
										<IsDataset>false</IsDataset>
									</AnyType>
									<AnyType xsi:type='typens:RasterFunctionVariable'>
										<Name>OutputValues_2018226_215812_169</Name>
										<Description/>
										<Value xsi:type='typens:ArrayOfDouble'>{RANKS}
										</Value>
										<IsDataset>false</IsDataset>
									</AnyType>
									<AnyType xsi:type='typens:RasterFunctionVariable'>
										<Name>NoDataRanges_2018226_215812_169</Name>
										<Description/>
										<Value xsi:type='typens:ArrayOfDouble'/>
										<IsDataset>false</IsDataset>
									</AnyType>
									<AnyType xsi:type='typens:RasterFunctionVariable'>
										<Name>AllowUnmatched_2018226_215812_169</Name>
										<Description/>
										<Value xsi:type='xs:boolean'>false</Value>
										<IsDataset>false</IsDataset>
									</AnyType>
								</Values>
							</Arguments>
							<Help/>
							<Type>0</Type>
							<Thumbnail/>
							<Definition/>
							<Group/>
							<Tag/>
							<ThumbnailEx/>
						</Argument>'''


DOUBLE_TEMPLATE = '''\n											<Double>{0}</Double>'''
				
lines = INPUT_STRING.split('\n')
rasString = ''
mathList = []
for line in lines:
	rasVars = {}
	breakString = ''
	rankString = ''
	info = line.split(' ')
	name = 'b'+info[0]
	weight = info[1]
	filePath = info[2]
	rasVars['NAME'] = name
	rasVars['PATH'],rasVars['FILE'] = os.path.split(filePath)
	for i in info[3:]:
		step = i.split(',')
		breakString+=DOUBLE_TEMPLATE.format(step[0])
		breakString+=DOUBLE_TEMPLATE.format(step[1])
		rankString+=DOUBLE_TEMPLATE.format(step[2])
	rasVars['BREAKS'] = breakString
	rasVars['RANKS'] = rankString
	# for i in rasVars:
		# print i, rasVars[i]
	# print ''
	
	rasString+=RASTER_TEMPLATE.format(**rasVars)
	
	math = '{0}*{1}'.format(name,weight)
	mathList.append(math)

mathString = '+'.join(mathList)
# print mathString
# print rasString


vatString = VAT_TEMPLATE.format(rasString,mathString)

print vatString

vatTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
vatPath = 'Q:\TEST\VATtest\VATtest_'+vatTime+'.rft.xml'
vatFile = open(vatPath, "w")
vatFile.write(vatString)
vatFile.close()

# arcpy.GenerateRasterFromRasterFunction_management(raster_function="Q:/TEST/VATtest/VATtest_20180227152122.rft.xml", 
	# out_raster_dataset="D:/VATtest/VATtest_fromfunction3.tif", 
	# raster_function_arguments="", 
	# raster_properties="", 
	# format="TIFF")
	
outTif = r'Q:/test/VATtest/VATtest_fromfunction7'+vatTime+'.tif'

raw_input('press enter to create raster')

t0 = time.time()

arcpy.GenerateRasterFromRasterFunction_management(raster_function=vatString, 
	out_raster_dataset=outTif, 
	raster_function_arguments="", 
	raster_properties="", 
	format="TIFF")
	
print 'all done'
print t0-time.time()