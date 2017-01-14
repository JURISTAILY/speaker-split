#-------------------------------------------------
#
# Project created by QtCreator 2016-12-30T16:42:56
#
#-------------------------------------------------

QT       += core gui

QT -= gui


greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11 console
CONFIG -= app_bundle

debug {
    QT += gui
    CONFIG += app_bundle
    CONFIG -= console
}

TARGET = speaker-split
TEMPLATE = app


SOURCES += *.cpp

SOURCES += \
    kernel/cvector.cpp \
    kernel/csize.cpp \
    kernel/crange.cpp \
    kernel/cmatrix.cpp \
    kernel/carray.cpp

HEADERS  += *.h

HEADERS  += \
    kernel/carray.h \
    kernel/cmatrix.h \
    kernel/crange.h \
    kernel/csize.h \
    kernel/cvector.h
