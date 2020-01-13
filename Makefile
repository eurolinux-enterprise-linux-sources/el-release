package = el-release
package_version_tar = $(shell spectool -l $(package).spec | grep Source0 |  awk -FSource0: '{print $$2}' | sed -e 's/^[ \t]*//')
package_version = $(shell echo $(package_version_tar) | awk -F.tar '{print $$1}')


sources:
	cp -a src $(package_version) \
	&& tar czvvf $(package_version_tar) $(package_version)/ \
	&& rm -rf $(package_version)
