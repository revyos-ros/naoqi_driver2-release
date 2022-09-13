%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/galactic/.*$
%global __requires_exclude_from ^/opt/ros/galactic/.*$

Name:           ros-galactic-naoqi-driver
Version:        2.0.0
Release:        0%{?dist}%{?release_suffix}
Summary:        ROS naoqi_driver package

License:        BSD
Source0:        %{name}-%{version}.tar.gz

Requires:       boost-devel
Requires:       boost-python%{python3_pkgversion}-devel
Requires:       ros-galactic-cv-bridge
Requires:       ros-galactic-image-transport
Requires:       ros-galactic-kdl-parser
Requires:       ros-galactic-naoqi-bridge-msgs >= 2.0.0
Requires:       ros-galactic-naoqi-libqi
Requires:       ros-galactic-naoqi-libqicore
Requires:       ros-galactic-orocos-kdl
Requires:       ros-galactic-rclcpp
Requires:       ros-galactic-robot-state-publisher
Requires:       ros-galactic-tf2-ros
Requires:       ros-galactic-ros-workspace
BuildRequires:  boost-devel
BuildRequires:  boost-python%{python3_pkgversion}-devel
BuildRequires:  ros-galactic-ament-cmake
BuildRequires:  ros-galactic-cv-bridge
BuildRequires:  ros-galactic-diagnostic-msgs
BuildRequires:  ros-galactic-diagnostic-updater
BuildRequires:  ros-galactic-geometry-msgs
BuildRequires:  ros-galactic-image-transport
BuildRequires:  ros-galactic-kdl-parser
BuildRequires:  ros-galactic-naoqi-bridge-msgs >= 2.0.0
BuildRequires:  ros-galactic-naoqi-libqi
BuildRequires:  ros-galactic-naoqi-libqicore
BuildRequires:  ros-galactic-orocos-kdl
BuildRequires:  ros-galactic-rclcpp
BuildRequires:  ros-galactic-robot-state-publisher
BuildRequires:  ros-galactic-sensor-msgs
BuildRequires:  ros-galactic-tf2-geometry-msgs
BuildRequires:  ros-galactic-tf2-msgs
BuildRequires:  ros-galactic-tf2-ros
BuildRequires:  ros-galactic-ros-workspace
Conflicts:      ros-galactic-nao-driver
Conflicts:      ros-galactic-naoqi-rosbridge
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-galactic-ament-lint-auto
BuildRequires:  ros-galactic-ament-lint-common
%endif

%description
Driver module between Aldebaran's NAOqiOS and ROS2. It publishes all sensor and
actuator data as well as basic diagnostic for battery, temperature. It
subscribes also to RVIZ simple goal and cmd_vel for teleop.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/galactic" \
    -DAMENT_PREFIX_PATH="/opt/ros/galactic" \
    -DCMAKE_PREFIX_PATH="/opt/ros/galactic" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/galactic

%changelog
* Tue Sep 13 2022 Marine Chamoux <mchamoux@softbankrobotics.com> - 2.0.0-0
- Autogenerated by Bloom

