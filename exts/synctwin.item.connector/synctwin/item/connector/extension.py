import omni.ext
import omni.ui as ui
from pathlib import Path
import carb.settings
import os 
import webbrowser
from enum import IntEnum

from pxr import Usd, Sdf, Gf, UsdGeom
from synctwin.item.connector.item_engineering_connector import ItemEngineeringConnector
ICON_PATH = Path(__file__).parent.parent.parent.parent.joinpath("data")

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class LevelOfDetail(IntEnum):
    LOW = 0,
    MEDIUM = 1,
    HIGH = 2 

class ItemConnectorExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    
    def _open_or_create_stage(self, path, clear_exist=False):
            if self._usd_context.open_stage(path):
                stage = omni.usd.get_context().get_stage()                
            else:
                omni.usd.get_context().new_stage()
                stage = omni.usd.get_context().get_stage()
                stage.SaveAs(path)
            if clear_exist: 
                stage.GetRootLayer().Clear()
            return stage



    def createInMemoryStage(path):
        
        if os.path.isfile(path):
            stage = Usd.Stage.Open(path)
        else:
            stage = Usd.Stage.CreateNew(path)
            UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
        return stage

    def project_url(self, project_id): 
        return f"{self._itemtool_url}/{project_id}"

    def project_usdpath(self, project_id, level_of_detail):
        if level_of_detail is None:
            return f"{self._projects_path}/{project_id}.usd"
        else:
            return f"{self._projects_path}/{project_id}/lod_{level_of_detail}.usd"
    
    def on_startup(self, ext_id):
        self._usd_context = omni.usd.get_context()
        self._selection = self._usd_context.get_selection()
        self._events = self._usd_context.get_stage_event_stream()
        self._stage_event_sub = self._events.create_subscription_to_pop(
            self._on_stage_event, name="on stage event synctwin item connector"
        )         
        self._item = ItemEngineeringConnector()     
        self._settings = carb.settings.get_settings()
        self._projects_path = self._settings.get("projects_path")                
        self._parts_path = self._settings.get("parts_path")
        self._itemtool_url= self._settings.get("itemtool_url")
        self._project_id = "1d05717eb87cec4287ed241312306c5f4"        

        print("[synctwin.item.connector] synctwin item startup")

        self._window = ui.Window("synctwin item connector", width=300, height=200)
        
       

            
        #omni.usd.get_context().new_stage()
        #stage = omni.usd.get_context().get_stage()

        with self._window.frame:
            with ui.VStack():
                
                with ui.HStack():                    
                    
                    omni.ui.Image(f'{ICON_PATH}/item_logo.png', width=80)
                    with ui.VStack():
                        ui.Spacer()                        
                        ui.Button("...", width=25, height=25, tooltip="open engineering tool in browser", clicked_fn=lambda: on_browser_click())
                        ui.Spacer()
                    ui.Spacer()
                ui.Label("Project-ID")
                project_field = ui.StringField(height=30)
                project_field.model.set_value(self._project_id)
                project_field.model.add_end_edit_fn(lambda new_value: on_project_edit(new_value))
                ui.Button("update", height=40, clicked_fn=lambda: on_update_click())
                def on_project_edit(new_value):
                    print("new value:", new_value.as_string)
                    self._project_id = new_value.as_string
                def on_update_click():
                    self.create_or_update_project_stage()
                def on_browser_click():
                    self.open_browser(self.project_url(self._project_id))
                    
                ui.Spacer()
        path = self._item.import_project(self._project_id)
        omni.usd.get_context().open_stage(path)

                

    def on_shutdown(self):
        print("[synctwin.item.connector] synctwin item shutdown")

    def _on_stage_event(self, event):
        """Called with subscription to pop"""

        if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
           self._on_selection_changed()

    def _on_selection_changed(self):
        """Called when the user changes the selection"""
        selection = self._selection.get_selected_prim_paths()
        stage = self._usd_context.get_stage()
        print("selection", selection )
        print("stage", stage)
        if selection and stage:
            prim = stage.GetPrimAtPath(selection[0])
            properties = prim.GetPropertyNames()
            #print(properties)
            print(prim.GetCustomData())           
    def open_browser(self, url):        
        webbrowser.open(url)

    def create_lodstage(self, level_of_detail):
        stage_path = self.project_usdpath(self._project_id, level_of_detail)
        stage = self._open_or_create_stage(stage_path, True)
        
        world = stage.DefinePrim("/World", "Xform")        
        cube = stage.DefinePrim("/World/cube", "Cube")
        cube.GetAttribute("size").Set(2.0)
        stage.SetDefaultPrim(world)
        stage.Save()
        #print(stage.GetRootLayer().ExportToString())
        return stage_path


    def create_or_update_project_stage(self):
        low_path = self.create_lodstage(LevelOfDetail.LOW)
        
        stage_path = self.project_usdpath(self._project_id, None)
        project_id = self._project_id
        # open and clear stage 
        stage = self._open_or_create_stage(stage_path, True)
        world = stage.DefinePrim("/World", "Xform")        
        stage.SetDefaultPrim(world)
        prim_path = f"/World/ie_{project_id}"
        model_prim = stage.DefinePrim(prim_path, "component")
        vset = model_prim.GetVariantSets().AddVariantSet('levelOfDetail')
        # Create variant options.
        vset.AddVariant('Low')        
        vset.AddVariant('Medium')
        vset.AddVariant('High') 

        vset.SetVariantSelection('Low')
        with vset.GetVariantEditContext():
            model_prim.GetReferences().AddReference(low_path)
        
        




         
        
        