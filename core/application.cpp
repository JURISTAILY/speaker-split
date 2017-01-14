#include "application.h"
#include <QDebug>
#include <QStringList>

Application::Application(int argc, char** argv)
    :
#ifndef QT_NO_DEBUG
        QApplication
#else
        QCoreApplication
#endif
            (argc, argv)
    #ifdef QT_NO_DEBUG
    , data(([](){
        const QStringList arg(QCoreApplication::arguments());
        if (arg.size() <= 1) {
            qFatal("enter input file name");
        }
        return TrainingSet(arg.back());
    })())
    #else
    , data("../../data.json")
    #endif
{
}

const TrainingSet& Application::trainingSet()
{
    return static_cast<Application*>(qApp)->data;
}

const QString Application::outFileName(const QString& suffix)
{
#ifdef QT_NO_DEBUG
    const QStringList f(QCoreApplication::arguments().back().split('.'));
    return f.begin() + '_' + suffix + '.' + f.back();
#else
    return QString("../../data_%1.json").arg(suffix);
#endif
}
