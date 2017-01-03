#include "application.h"
#include "neuralcompressor.h"

#include <QJsonDocument>
#include <QJsonArray>
#include <QFile>

int main(int argc, char *argv[])
{
    Application a(argc, argv);

    NeuralCompressor classificator(Application::trainingSet(), 2);

    QFile outFile(Application::outFileName("out"));
    if (!outFile.open(QFile::WriteOnly)) {
        qFatal("Can't write out file");
    }
    outFile.write(QJsonDocument(classificator.classify(Application::trainingSet())).toJson());

    a.quit();
    return 0;
}
