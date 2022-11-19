import type{ NavItems } from './types'

export const NAV_ITEMS: NavItems = {
    home: {
        path: '/',
        title: 'home'
    },
    blog: {
        path: '/blog',
        title: 'blog'
    },
    tags: {
        path: '/tags',
        title: 'tags'
    },
    about: {
        path: '/about',
        title: 'about'
    }
}

export const SITE = {
    // Your site's detail?
    name: 'Art Fewell\'s Blog',
    title: 'Art Fewell\'s Blog',
    description: 'This site provides words, sentences, and paragraphs - all at no extra charge',
    url: 'https://artfewell.com',
    githubUrl: 'https://github.com/afewell',
    listDrafts: true
    // description ?
}

export const PAGE_SIZE = 8
