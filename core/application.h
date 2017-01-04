#ifndef APPLICATION_H
#define APPLICATION_H

#ifndef QT_NO_DEBUG
#include <QApplication>
#else
#include <QCoreApplication>
#endif
#include "trainingset.h"

class Application : public
#ifndef QT_NO_DEBUG
        QApplication
        #else
        QCoreApplication
        #endif
{
    const TrainingSet data;
public:
    Application(int argc, char** argv);

    static const TrainingSet &trainingSet();
    static const QString outFileName(const QString& suffix);
};

#endif // APPLICATION_H
