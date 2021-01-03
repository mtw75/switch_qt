#include "view.h"
#include <pxr/imaging/glf/glew.h>
#include "Scene.h"
#include <QDebug>
#include <QTimer>
#include <QMouseEvent>

View::View(QWidget* parent) : QOpenGLWidget(parent) { 
    setMouseTracking(true);
}

 View::~View() { if (m_scene) delete(m_scene); }

 void View::initializeGL()
{
    // Set up the rendering context, load shaders and other resources, etc.:
    QOpenGLFunctions* f = QOpenGLContext::currentContext()->functions();
    f->glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
    m_elapsed.start();
    // init usd after we've been initialized 
    m_scene = new Scene;
}

inline void View::paintGL()
{
    QOpenGLFunctions* f = QOpenGLContext::currentContext()->functions();
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LESS);

    glEnable(GL_BLEND);

    
    m_scene->prepare(m_elapsed.elapsed()/100.0f);
    m_scene->draw(width(), height());
    m_elapsed.restart();
    update();    
}

void View::mouseMoveEvent(QMouseEvent* event)
{
    m_scene->cursor(event->x()/(float)width(), event->y()/(float)height());

}

void View::mousePressEvent(QMouseEvent* event)
{
    m_scene->click();
}
