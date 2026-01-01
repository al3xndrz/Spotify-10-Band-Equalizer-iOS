ARCHS = arm64e
TARGET := iphone:clang:latest:15.0

include $(THEOS)/makefiles/common.mk

LIBRARY_NAME = SpotifyEQ10

SpotifyEQ10_FILES = Tweak.m
SpotifyEQ10_CFLAGS = -fobjc-arc
SpotifyEQ10_FRAMEWORKS = Foundation UIKit

include $(THEOS_MAKE_PATH)/library.mk
