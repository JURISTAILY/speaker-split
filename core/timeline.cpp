#ifndef QT_NO_DEBUG
#include "timeline.h"

#include <QPainter>

Timeline::Timeline(QWidget *parent)
    : QWidget(parent)
{

}

void Timeline::paintEvent(QPaintEvent*)
{
    if (data.size() < 2) {
        return;
    }
    QPainter painter(this);

    const double k(timeDelay() / this->width());

    double cur(std::numeric_limits<double>::quiet_NaN());
    double prev;

    for (QMap<double, QPair<int, bool>>::const_iterator it(data.begin()); it != data.end(); ++it) {
        const QPair<double, QPair<int, bool> > sample(it.key(), it.value());
        prev = cur;
        cur = (sample.first - timeBegin()) / k;
        if (std::isfinite(prev)) {
            painter.fillRect(QRectF(QPointF(prev, 0), QPointF(cur, this->height())), classToColor(sample.second));
        }
    }
    painter.fillRect(QRectF(QPointF(cur, 0), QPointF(timeEnd() / k, this->height())), classToColor(data.last()));
}

QColor Timeline::classToColor(QPair<int, bool> c)
{
    static const QRgb defoultColorsCludge[] = { 0xFF880000, 0xFF008800, 0xFF000088,
                                                0xFF888800, 0xFF880088, 0xFF008888,
                                                0xFF88FFFF, 0xFFFF88FF, 0xFFFFFF88,
                                                0xFF8888FF, 0xFF88FF88, 0xFFFF8888 };
    return c.second ? defoultColorsCludge[c.first] : QColor(Qt::black);
}

double Timeline::timeEnd() const
{
    return (data.lastKey() - data.firstKey()) / (data.size() - 1) + data.lastKey();
}

double Timeline::timeBegin() const
{
    return data.firstKey();
}

double Timeline::timeDelay() const
{
    return timeEnd() - timeBegin();
}

void Timeline::setData(const QMap<double, QPair<int, bool>>& d)
{
    data = d;
    this->update();
}

#endif // QT_NO_DEBUG
