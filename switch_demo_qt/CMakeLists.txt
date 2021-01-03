
set(CMAKE_VERBOSE_MAKEFILE ON)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

add_executable(switch_demo_qt main.cpp scene.h scene.cpp view.cxx view.h)


target_link_libraries(switch_demo_qt 
    PUBLIC
    opengl32 
    Qt5::Core
    Qt5::Gui
    Qt5::Widgets
    ext::glew
    ext::python
    ext::nv-usd    
    
)
install(TARGETS switch_demo_qt DESTINATION . ) 

install(FILES  switch.usda switch.ma board.usda  DESTINATION . )

WinDeployQt(TARGET switch_demo_qt QMLDIR ${CMAKE_CURRENT_SOURCE_DIR})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/../../windeployqt/ DESTINATION . )
