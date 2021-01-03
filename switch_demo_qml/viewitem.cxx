#include "viewitem.h"

#include <QDebug>
#include <QTimer>
#include <QMouseEvent>
#include <QQuickWindow>


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
    int width=size.width(); 
    int height=size.height();
    m_scene->draw(width, height);
    m_elapsed.restart();
    update();    
}
