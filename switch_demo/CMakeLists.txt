
set(CMAKE_VERBOSE_MAKEFILE ON)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

add_executable(switch_demo main.cpp scene.h scene.cpp )


target_link_libraries(switch_demo 
    PUBLIC
    opengl32 
    ext::glfw
    ext::glew
    ext::python
    ext::nv-usd    
    
)
install(TARGETS switch_demo DESTINATION . ) 

install(FILES  switch.usda switch.ma board.usda  DESTINATION . )