import { StalkerPyramidPage } from './app.po';

describe('stalker_pyramid App', () => {
  let page: StalkerPyramidPage;

  beforeEach(() => {
    page = new StalkerPyramidPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!!');
  });
});
