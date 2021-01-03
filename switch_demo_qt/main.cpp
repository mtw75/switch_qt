#include "scene.h"


#include <boost/predef/os.h>
#include <pxr/base/gf/camera.h>
#include <pxr/base/js/json.h>
#include <pxr/base/plug/plugin.h>
#include <pxr/base/tf/fileUtils.h>
#include <pxr/pxr.h>
#include <pxr/usd/usd/inherits.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/xformable.h>


#include <fstream>
#include <streambuf>
#include <QOpenGLWidget> 
#include <QDebug>
#include <QDir>
#include <QApplication>
#include "View.h"

PXR_NAMESPACE_USING_DIRECTIVE

// Window dimensions.
#define WIDTH 1280
#define HEIGHT 960

double scale = 150.0;
Scene* scene = NULL;

//// Is called whenever a key is pressed/released via GLFW.
//void key_callback(
//        GLFWwindow* window, int key, int scancode, int action, int mode)
//{
//    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
//        glfwSetWindowShouldClose(window, GL_TRUE);
//}
//
//// Is called scrolled via GLFW.
//void scroll_callback(GLFWwindow* window, double xoffset, double yoffset)
//{
//    scale *= pow(1.1, -yoffset);
//}
//
//void mouseButtonCallback(
//        GLFWwindow* window, int button, int action, int mods)
//{
//    if (scene && action == GLFW_PRESS)
//    {
//        scene->click();
//    }
//}
//
//void cursorPosCallback(
//        GLFWwindow* window, double xpos, double ypos)
//{
//    if (scene)
//    {
//        int width, height;
//        glfwGetWindowSize(window, &width, &height);
//
//        scene->cursor(xpos/width, ypos/height);
//    }
//}

int main(int argc, char **argv)
{
    qputenv("QML_DISABLE_DISK_CACHE", "true");
    qputenv("PATH", qPrintable(QDir::currentPath()));
    qputenv("QML2_IMPORT_PATH", qPrintable(QDir::currentPath()));
    qputenv("QT_PLUGIN_PATH", qPrintable(QDir::currentPath()));
    qDebug() << "hello";
    QApplication app(argc, argv);
    
    View view;
    view.show();
    return app.exec();
    //// Create a GLFWwindow object that we can use for GLFW's functions.
    //GLFWwindow* window = glfwCreateWindow(WIDTH, HEIGHT, "Switch", NULL, NULL);
    //if (!window)
    //{
    //    printf("Can't create GLFW context\n");
    //    glfwTerminate();
    //    return 1;
    //}

    //glfwMakeContextCurrent(window);

    //// Set the required callback functions.
    //glfwSetKeyCallback(window, key_callback);
    //glfwSetScrollCallback(window, scroll_callback);
    //glfwSetMouseButtonCallback(window, mouseButtonCallback);
    //glfwSetCursorPosCallback(window, cursorPosCallback);

    //// Set this to true so GLEW knows to use a modern approach to retrieving
    //// function pointers and extensions.
    //glewExperimental = GL_TRUE;
    //// Initialize GLEW to setup the OpenGL Function pointers.
    //GlfGlewInit();

    //scene = new Scene;

    //double timer = glfwGetTime();

    //// Game loop
    //while (!glfwWindowShouldClose(window))
    //{
    //    // Check if any events have been activiated (key pressed, mouse moved
    //    // etc.) and call corresponding response functions.
    //    glfwPollEvents();
    //    
    //    double now = glfwGetTime();
    //    scene->prepare(now - timer);
    //    timer = now;

    //    int width, height;
    //    glfwGetFramebufferSize(window, &width, &height);

    //    glViewport(0, 0, width, height);
    //    //printf("render %d %d\n", width, height);
    //    glEnable(GL_DEPTH_TEST);
    //    glDepthFunc(GL_LESS);

    //    glEnable(GL_BLEND);

    //    // Render
    //    // Clear the colorbuffer.
    //    glClearColor(0.5f, 0.5f, 0.5f, 1.0f);
    //    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    //    scene->draw(width, height);

    //    // Swap the screen buffers.
    //    glfwSwapBuffers(window);
    //}

    //delete scene;

    //// Terminate GLFW, clearing any resources allocated by GLFW.
    //glfwTerminate();
    //return 0;
}
