#pragma once 
#define QT_NO_KEYWORDS
#include <pxr/imaging/glf/glew.h>
#include "Scene.h"
#include <QMatrix4x4>
#include <QOpenGLFunctions>
#include <QElapsedTimer>
#include <QQuickFramebufferObject>
#include <QOpenGLFramebufferObject>

class ViewItem;

class FbItemRenderer : public QQuickFramebufferObject::Renderer
{
public:
    QOpenGLFramebufferObject* createFramebufferObject(const QSize& size)
    {
        QOpenGLFramebufferObjectFormat format;
        format.setAttachment(QOpenGLFramebufferObject::CombinedDepthStencil);
        // optionally enable multisampling by doing format.setSamples(4);
        return new QOpenGLFramebufferObject(size, format);
    }
    void render();
    FbItemRenderer(const ViewItem * const item)  {
        m_item = item; 
    }
    Scene* m_scene = nullptr;
    QElapsedTimer m_elapsed;
    const ViewItem* m_item =nullptr; 
};


class ViewItem : public QQuickFramebufferObject     
{
     
public:
    ViewItem() {
        setMirrorVertically(true);
    }

    QQuickFramebufferObject::Renderer* createRenderer() const
    {
        return new FbItemRenderer(this);
    }

};

