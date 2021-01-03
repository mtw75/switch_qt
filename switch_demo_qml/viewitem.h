#pragma once 
#define QT_NO_KEYWORDS
#include <pxr/imaging/glf/glew.h>
#include "Scene.h"
#include <QMatrix4x4>
#include <QPointF>
#include <QOpenGLFunctions>
#include <QElapsedTimer>
#include <QQuickFramebufferObject>
#include <QOpenGLFramebufferObject>

class ViewItem;

class FbItemRenderer : public QQuickFramebufferObject::Renderer
{
public:
    FbItemRenderer();
    QOpenGLFramebufferObject* createFramebufferObject(const QSize& size);
    void render() override;    
    void	synchronize(QQuickFramebufferObject* item) override;
protected:
    Scene* m_scene = nullptr;
    qint64 m_prevTime=0; 
    QElapsedTimer m_timer;
    QPointF m_mousePosition;
    bool m_buttonPressed = false;
};


class ViewItem : public QQuickFramebufferObject     
{
     
public:
    ViewItem();

    QQuickFramebufferObject::Renderer* createRenderer() const;
    void	mouseMoveEvent(QMouseEvent* event) override;
    void	mousePressEvent(QMouseEvent* event) override;
    void	mouseReleaseEvent(QMouseEvent* event) override;
    void hoverMoveEvent(QHoverEvent* event) override;
    const QPoint& mousePosition() { return m_mousePosition;  }
    bool buttonPressed() { return m_buttonPressed;  }
protected:
    QPoint m_mousePosition; 
    bool m_buttonPressed=false;
   
};

