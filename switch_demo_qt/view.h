#pragma once 
#include <pxr/imaging/glf/glew.h>
#define QT_NO_KEYWORDS
#include <QOpenGLWidget>
#include <QMatrix4x4>
#include <QOpenGLFunctions>
#include <QElapsedTimer>

class Scene;

class View : public QOpenGLWidget
{
public:
    View(QWidget* parent=nullptr);
    ~View();
protected:
    void initializeGL() override;
    void paintGL() override;
    void	mouseMoveEvent(QMouseEvent* event) override;
    void	mousePressEvent(QMouseEvent* event) override; 
    Scene *m_scene = nullptr;
    QElapsedTimer m_elapsed;
};