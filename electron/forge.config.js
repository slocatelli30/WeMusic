module.exports = {
  packagerConfig: {
    icon: 'img/icon',
  },
  rebuildConfig: {},
  makers: [
    {
      name: '@electron-forge/maker-zip',
      // platforms: ['darwin'],
      icon: 'img/icon.ico',
    },
    // {
    //   name: '@electron-forge/maker-deb',
    //   config: {},
    // },
    {
      name: '@electron-forge/maker-squirrel',
      config: {
        certificateFile: './cert.pfx',
        certificatePassword: process.env.CERTIFICATE_PASSWORD,
        setupIcon: 'img/icon.ico',
      },
    },
  ],
};
