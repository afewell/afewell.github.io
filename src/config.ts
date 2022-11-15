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
    name: 'The Art of Tanzu',
    title: 'The Art of Tanzu',
    description: 'Stuff about Tanzu. Powered by Tanzu. Personal site, opinions are my own',
    url: 'https://blog.tanzu.art',
    githubUrl: 'https://github.com/artoftanzu/blog',
    listDrafts: true
    // description ?
}

export const PAGE_SIZE = 8
