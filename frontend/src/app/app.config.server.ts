import { mergeApplicationConfig, ApplicationConfig } from '@angular/core';
import { provideServerRendering, RenderMode, withRoutes } from '@angular/ssr';
import { appConfig } from './app.config';
import { serverRoutes } from './app.routes.server';

const serverConfig: ApplicationConfig = {
  // providers: [
  //   provideServerRendering(withRoutes(serverRoutes))
  // ]

  providers: [
    provideServerRendering(
      withRoutes([
        {
          path: 'tower/:code',
          renderMode: RenderMode.Server
        },
        {
          path: '**',
          renderMode: RenderMode.Server 
        }
      ])
    )
  ]
};

export const config = mergeApplicationConfig(appConfig, serverConfig);
