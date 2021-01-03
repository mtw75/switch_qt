#include "viewitem.h"

#include <QDebug>
#include <QTimer>
#include <QMouseEvent>
#include <QQuickWindow>

//
//View::View(QWidget* parent) : QOpenGLWidget(parent) { 
//    setMouseTracking(true);
//}
//
// View::~View() { if (m_scene) delete(m_scene); }
//
// void View::initializeGL()
//{
//    // Set up the rendering context, load shaders and other resources, etc.:
//    QOpenGLFunctions* f = QOpenGLContext::currentContext()->functions();
//    f->glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
//    m_elapsed.start();
//    // init usd after we've been initialized 
//    m_scene = new Scene;
//}
//
//inline void View::paintGL()
//{
//    QOpenGLFunctions* f = QOpenGLContext::currentContext()->functions();
//    glEnable(GL_DEPTH_TEST);
//    glDepthFunc(GL_LESS);
//
//    glEnable(GL_BLEND);
//
//    
//    m_scene->prepare(m_elapsed.elapsed()/100.0f);
//    m_scene->draw(width(), height());
//    m_elapsed.restart();
//    update();    
//}
//
//void View::mouseMoveEvent(QMouseEvent* event)
//{
//    m_scene->cursor(event->x()/(float)width(), event->y()/(float)height());
//
//}
//
//void View::mousePressEvent(QMouseEvent* event)
//{
//    m_scene->click();
//}

 void FbItemRenderer::render()
{
     if (!m_scene) {         
        m_scene = new Scene;
     }
     // Clear the colorbuffer.
     glClearColor(0.5f, 0.5f, 0.5f, 1.0f);
     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

     glEnable(GL_DEPTH_TEST);
     glDepthFunc(GL_LESS);
     
     glEnable(GL_BLEND);
     
    m_scene->prepare(m_elapsed.elapsed() / 100.0f);
    QSize size = framebufferObject()->size();
    int width=size.width(); int height=size.height();
    m_scene->draw(width, height);
    m_elapsed.restart();
    update();
    //m_item->window()->resetOpenGLState();
}
