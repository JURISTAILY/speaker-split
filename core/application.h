#ifndef APPLICATION_H
#define APPLICATION_H

#include <QCoreApplication>
#include "trainingset.h"

class Application : public QCoreApplication
{
    const TrainingSet data;
public:
    Application(int argc, char** argv);

    static const TrainingSet &trainingSet();
    static const QString outFileName(const QString& suffix);
};

#endif // APPLICATION_H
