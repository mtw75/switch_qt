from pxr import Usd, Sdf, UsdGeom
from enum import IntEnum

class LevelOfDetail(IntEnum):
    LOW = 0,
    MEDIUM = 1,
    HIGH = 2 

class ItemEngineeringConnector:
    _itemtool_url = "https://item.engineering/DEde/tools/engineeringtool"    
    _projects_path = "omniverse://ovnuc/Projects/BMW_MIRROR/ConnectedSystems/item_engineering_tool"
    _parts_path = "omniverse://ovnuc/Projects/BMW_MIRROR/ConnectedSystems/item_engineering_tool/parts"

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

    def create_lod_stage(self, project_id, lod):
        lod_stage_path = f"{self._projects_path}/{project_id}/lod{lod}.usd"        
        lod_stage = self._open_or_create_stage(lod_stage_path)
        lod_world = lod_stage.DefinePrim("/World", "Xform")        
        cube = lod_stage.DefinePrim("/World/cube", "Cube")
        UsdGeom.SetStageUpAxis(lod_stage, UsdGeom.Tokens.y)        
        cube.GetAttribute("size").Set(2.0)
        lod_stage.SetDefaultPrim(lod_world)
        lod_stage.Save()
        #print(lod_stage.GetRootLayer().ExportToString())
        return f"{project_id}/lod{lod}.usd"
        
    def import_project(self, project_id):
        print("\n\n=================")
        

        
        
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
            item_prim.GetReferences().AddReference(self.create_lod_stage(project_id, LevelOfDetail.LOW))
        vset.SetVariantSelection('Medium')
        with vset.GetVariantEditContext():            
            item_prim.GetReferences().AddReference(self.create_lod_stage(project_id, LevelOfDetail.MEDIUM))            
        vset.SetVariantSelection('High')
        with vset.GetVariantEditContext():            
            item_prim.GetReferences().AddReference(self.create_lod_stage(project_id, LevelOfDetail.HIGH))            
        stage.Save()
        print(stage.GetRootLayer().ExportToString())
        print("written.")
        return stage_path

    