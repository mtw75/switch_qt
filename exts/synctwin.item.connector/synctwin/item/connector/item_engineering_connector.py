from pxr import Usd, Sdf, UsdGeom, Gf
from enum import IntEnum
import omni.services.client as OmniServicesClient
import omni.kit
import omni.client as OmniClient
import omni.ui as ui
import tempfile
import carb
import asyncio
import json 
import webbrowser

class LevelOfDetail(IntEnum):
    LOW = 0,
    MEDIUM = 1,
    HIGH = 2 

class ItemEngineeringConnector:
    _item_host = "https://item.engineering"
    _item_itemtool_url = "DEde/tools/engineeringtool"    
    _item_geometry_info_endpoint = "dqart/0:DEde/project_utilities/get_geometry_info"
    _item_object_pool_data_endpoint = "objectPoolData"

    _projects_path = "c:/temp/item_engineering_tool"
    _parts_path = "c:/temp/item_engineering_tool/parts"
    #_projects_path = "omniverse://ovnuc/Projects/BMW_MIRROR/ConnectedSystems/item_engineering_tool"
    #_parts_path = "omniverse://ovnuc/Projects/BMW_MIRROR/ConnectedSystems/item_engineering_tool/parts"
    
    def __init__(self):
        self._omni_client = OmniServicesClient.AsyncClient(self._item_host) 

    def _open_or_create_stage(self, path, clear_exist=True):
        layer = Sdf.Layer.FindOrOpen(path)
        if not layer:
            layer = Sdf.Layer.CreateNew(path)
        elif clear_exist:
            layer.Clear()
            
        if layer:
            return Usd.Stage.Open(layer)
        else:
            return None

    def refresh_parts(self):
        self._ov_parts = []
        result, entries = OmniClient.list(self._parts_path)
        for entry in entries:
            self._ov_parts.append(entry.relative_path)
        print (f"parts refreshed, found: {len(self._ov_parts)}")

        
    def _show_waiting_popup_convert(self):
        if not self._waiting_popup_convert:
            self._waiting_popup_convert = ProgressPopup("Converting...", status_text="Preparing...")

        self._waiting_popup_convert.status_text = "Preparing..."
        self._waiting_popup_convert.progress = 0.0
        self._waiting_popup_convert.show()

    async def download_blob(self, temp_dir, geo_model, usd_filename):
        blob_url = f'/objectPoolData/{geo_model}'
        print(f"    download {blob_url}")                    
        blob = await self._omni_client.get(blob_url)
                        
        temp_blob_path =f"{temp_dir.name}/blob.obj" 
        blobfile = open(temp_blob_path, "wb") 
        blobfile.write(blob)
        blobfile.close()
                        
        print(f"written to temp: {temp_blob_path}")
                        

        converter_manager = omni.kit.asset_converter.get_instance()
        context = omni.kit.asset_converter.AssetConverterContext()
        context.ignore_materials = True                        
        output_path = f"{self._parts_path}/{usd_filename}"
        
        print("convert...")
        print("target:" + output_path)
        def convert_progress_callback(progress, total):
            print(f"convert progress: {float(progress) / total}")
        def material_loader(descr):
            print(f"material loader {descr}" )
        task = converter_manager.create_converter_task(temp_blob_path, output_path, convert_progress_callback, context, material_loader)
        success =  await task.wait_until_finished()
        print(f"success: {success}")
        if success:
            self._ov_parts.append(usd_filename)
        else:            
            detailed_status_code = task.get_status()
            detailed_status_error_string = task.get_detailed_error()
            print(f"error converting: {detailed_status_code} {detailed_status_error_string}...")
        return output_path

    async def _create_lod_stage(self, project_id, lod):
        print("create lod stage ...")
        lod_stage_path = f"{self._projects_path}/{project_id}/lod{lod}.usd"      
        rel_parts_path = "../parts"  
        lod_stage = self._open_or_create_stage(lod_stage_path)
        lod_world = lod_stage.DefinePrim("/World", "Xform")                
        UsdGeom.SetStageUpAxis(lod_stage, UsdGeom.Tokens.y)                
        lod_stage.SetDefaultPrim(lod_world)
        #-----------------------------------------
        with_product_info = 1        
        with_conveyor_info = 1
        with_material_info = 1
        url = f'{self._item_geometry_info_endpoint}/{project_id}/{lod}/{with_product_info}/{with_conveyor_info}/{with_material_info}'
        print("REQUEST->" + url)
        doc = await self._omni_client.get(url)

        #webbrowser.open(f"{self.item_host}/{url}")

        #print(json.dumps(doc)) 
        blobfile = open("c:\\temp\\out.jsn", "w") 
        blobfile.write(json.dumps(doc))
        blobfile.close()
        p_p_obj = doc['p']
        p_obj = p_p_obj['objects']
        pidx = 0
        temp_dir = tempfile.TemporaryDirectory()
        for part_id in p_obj.keys():
            
            part_obj = p_obj[part_id]
            part_group_id = part_obj['g_id']
            part_product_name = part_obj['name']
            part_article_number = part_obj.get('art', "")
            part_roller_conveyor = part_obj.get('roller_conveyor')
            part_length = part_obj.get('length')
            
            idx = 0 
            pidx = pidx + 1 
            part_g_obj = part_obj['g']
            print(f'PART {part_id} {pidx}/{ len(p_obj)} (geos:{len(part_g_obj)}): {part_product_name}')
            
            for geo_obj in part_g_obj:
                idx = idx + 1 

                geo_model = geo_obj['m']
                geo_scale = geo_obj['s']
                geo_position = geo_obj['p']
                geo_rotation = geo_obj['r']
                print(f'  geo {geo_model}')
                self.prim = None
                prim_path = f"/World/g_{part_group_id}/a_{part_article_number}_{pidx}/m_{idx}"
                if geo_model.endswith(".obj"):
                    print("   obj:")
                    usd_filename = f"g_{geo_model.replace('/','_')}_.usd"
                    if usd_filename in self._ov_parts:
                        print("     using library part")
                        output_path = f"{self._parts_path}/{usd_filename}"
                    else:
                        print("     downloading")
                        output_path = await self.download_blob(temp_dir, geo_model, usd_filename)
                    print("     d1")
                    model = lod_stage.DefinePrim(prim_path, "")
                    model.SetInstanceable(False)
                    print("     d2")
                    model_part = lod_stage.DefinePrim(prim_path+"/part", "")
                    print(f"     d3 {usd_filename}")
                    model_part.GetReferences().AddReference(f"{rel_parts_path}/{usd_filename}")
                    print("     d4")
                    
                    UsdGeom.Xformable(model_part).ClearXformOpOrder ()
                    UsdGeom.Xformable(model_part).AddTranslateOp().Set(Gf.Vec3f(geo_position["x"], geo_position["y"], geo_position["z"]))
                    UsdGeom.Xformable(model_part).AddRotateXYZOp().Set(Gf.Vec3f(geo_rotation["x"], geo_rotation["y"], geo_rotation["z"]))    
                    UsdGeom.Xformable(model_part).AddScaleOp().Set(Gf.Vec3f(geo_scale["x"], geo_scale["y"], geo_scale["z"]))    
                    print("    obj done.")
                elif geo_model == "cube":                    
                    print(prim_path)
                    cube = lod_stage.DefinePrim(prim_path, "Cube")
                    cube.GetAttribute("size").Set(2.0)
                    
                    UsdGeom.Xformable(cube).ClearXformOpOrder ()
                    UsdGeom.Xformable(cube).AddTranslateOp().Set(Gf.Vec3f(geo_position["x"], geo_position["y"], geo_position["z"]))
                    UsdGeom.Xformable(cube).AddRotateXYZOp().Set(Gf.Vec3f(geo_rotation["x"], geo_rotation["y"], geo_rotation["z"]))    
                    UsdGeom.Xformable(cube).AddScaleOp().Set(Gf.Vec3f(geo_scale["x"], geo_scale["y"], geo_scale["z"]))    

                elif geo_model == "cylinder":
                    cylinder = lod_stage.DefinePrim(prim_path, "Cylinder")
                    cylinder.GetAttribute("radius").Set(1.0)
                    cylinder.GetAttribute("axis").Set("Y")
                    cylinder.GetAttribute("height").Set(1.0)
                    
                    
                    UsdGeom.Xformable(cylinder).ClearXformOpOrder ()
                    UsdGeom.Xformable(cylinder).AddTranslateOp().Set(Gf.Vec3f(geo_position["x"], geo_position["y"], geo_position["z"]))
                    UsdGeom.Xformable(cylinder).AddRotateXYZOp().Set(Gf.Vec3f(geo_rotation["x"], geo_rotation["y"], geo_rotation["z"]))    
                    UsdGeom.Xformable(cylinder).AddScaleOp().Set(Gf.Vec3f(geo_scale["x"], geo_scale["y"], geo_scale["z"]))    
                else :
                    print(f"unknown geo type {geo_model}")

            print("done.")
        
        lod_stage.Save()
        #print(lod_stage.GetRootLayer().ExportToString()) 
        return f"{project_id}/lod{lod}.usd"

    async def _create_main_stage(self, project_id):
        stage_path = f"{self._projects_path}/{project_id}.usd"
        stage = self._open_or_create_stage(stage_path)
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y) 
        if stage is None:
            print("error creating stage")
            return None
        world_prim = stage.DefinePrim("/World", "Xform")         
        stage.SetDefaultPrim(world_prim)
        item_prim = stage.DefinePrim(f"/World/item_{project_id}", "")        
        vset = item_prim.GetVariantSets().AddVariantSet('LOD')
        # Create variant options.
        vset.AddVariant('Low')        
        vset.AddVariant('Medium')
        vset.AddVariant('High') 

        vset.SetVariantSelection('Low')
        with vset.GetVariantEditContext():       
            low_lod_path = await self._create_lod_stage(project_id, LevelOfDetail.LOW) 
            item_prim.GetReferences().AddReference(low_lod_path)
            
        vset.SetVariantSelection('Medium')
        with vset.GetVariantEditContext():       
            medium_lod_path = await self._create_lod_stage(project_id, LevelOfDetail.MEDIUM)     
            item_prim.GetReferences().AddReference(medium_lod_path)            
        vset.SetVariantSelection('High')
        with vset.GetVariantEditContext():            
            high_lod_path = await self._create_lod_stage(project_id, LevelOfDetail.HIGH)
            item_prim.GetReferences().AddReference(high_lod_path)            
        
        stage.Save()
        #print(stage.GetRootLayer().ExportToString())
        print(f"written.{stage_path}")
        return stage_path

    def import_project(self, project_id):
        print("\n\n IMPORT =================")
        
        self.refresh_parts()

        #loop = asyncio.get_event_loop()
        #try:
        #    result = loop.run_until_complete(asyncio.ensure_future(self._create_main_stage(project_id)))
        #    print(f"GOTI IT {result} ") 
        #finally:
        #    loop.close() 
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._create_main_stage(project_id)) # just some task
        r = loop.run_until_complete(task) # wait for it (outside of a coroutine)
        #r = asyncio.ensure_future(self._create_main_stage(project_id))

        print("ENSIRED")
        print(r)
        print("=================\n\n")
        return r
        

    