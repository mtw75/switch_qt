#include "viewitem.h"

#include <QDebug>
#include <QTimer>
#include <QMouseEvent>
#include <QHoverEvent>
#include <QQuickWindow>

FbItemRenderer::FbItemRenderer() {
    m_timer.start();
}

QOpenGLFramebufferObject* FbItemRenderer::createFramebufferObject(const QSize& size)
{
    QOpenGLFramebufferObjectFormat format;
    format.setAttachment(QOpenGLFramebufferObject::CombinedDepthStencil);
    format.setSamples(4);
    return new QOpenGLFramebufferObject(size, format);
}

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
     
     qint64 currTime = m_timer.elapsed();
    m_scene->prepare((currTime- m_prevTime)/1000.0f);
    QSize size = framebufferObject()->size();
    int width=size.width(); 
    int height=size.height();
    
    m_scene->draw(width, height);
    
    m_scene->cursor(m_mousePosition.x()/(float)width, m_mousePosition.y()/ (float)height);
    
    if (m_buttonPressed) {
        m_scene->click();
        m_buttonPressed = false;
    }
    m_prevTime = currTime; 
    
}



 void FbItemRenderer::synchronize(QQuickFramebufferObject* item) {
     QQuickFramebufferObject::Renderer::synchronize(item);
     if (ViewItem* viewItem = dynamic_cast<ViewItem*>(item)) {
         m_buttonPressed = viewItem->buttonPressed();
         m_mousePosition = viewItem->mousePosition();
     }
     item->update();
 }

 ViewItem::ViewItem() {
     setMirrorVertically(true);
     setAcceptHoverEvents(true);
     setFlag(ItemAcceptsInputMethod, true);
     setAcceptedMouseButtons(Qt::AllButtons);
 }

 QQuickFramebufferObject::Renderer* ViewItem::createRenderer() const
 {
     return new FbItemRenderer();
 }

 void ViewItem::mouseMoveEvent(QMouseEvent* event) {

    m_buttonPressed = false; 
 }

 void ViewItem::mousePressEvent(QMouseEvent* event) {
     m_buttonPressed = true; 
 }

 void ViewItem::mouseReleaseEvent(QMouseEvent* event) {
     m_buttonPressed = false;
 }

 void ViewItem::hoverMoveEvent(QHoverEvent* event) {
     QQuickItem::hoverMoveEvent(event);
     
     m_mousePosition = event->pos();
     update();
 }
