#ifndef TIMELINE_H
#define TIMELINE_H
#ifndef QT_NO_DEBUG
#include <QWidget>
#include <QMap>

class Timeline : public QWidget
{
    Q_OBJECT

    QMap<double, int> data;

    void paintEvent(QPaintEvent*) override;

    static QColor classToColor(int);
    double timeEnd() const;
    double timeBegin() const;
    double timeDelay() const;
public:
    explicit Timeline(QWidget *parent = 0);
    void setData(const QMap<double, int>&);


signals:

public slots:
};
#endif // QT_NO_DEBUG
#endif // TIMELINE_H
