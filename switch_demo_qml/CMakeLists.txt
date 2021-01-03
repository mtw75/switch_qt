
set(CMAKE_VERBOSE_MAKEFILE ON)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

file(GLOB_RECURSE QMLS . *.qml)
SOURCE_GROUP(qml FILES ${QMLS})
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
add_executable(switch_demo_qml main.cpp scene.h scene.cpp viewitem.cxx viewitem.h  ${QMLS} qml.qrc)


target_link_libraries(switch_demo_qml
    PUBLIC
    opengl32 
    Qt5::Core
    Qt5::Gui
    Qt5::Quick
    ext::glew
    ext::python
    ext::nv-usd    
    
)
install(TARGETS switch_demo_qml DESTINATION . ) 

install(FILES  switch.usda switch.ma board.usda  DESTINATION . )

WinDeployQt(TARGET switch_demo_qml QMLDIR ${CMAKE_CURRENT_SOURCE_DIR})
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/../../windeployqt/ DESTINATION . )
