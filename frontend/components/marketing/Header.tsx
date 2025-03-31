'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { useState, useEffect, useRef } from 'react';
import { appName, marketingNavItems } from '@/lib/consts';
import { cn } from '@/lib/utils';

export default function Header() {
	const [scrollState, setScrollState] = useState('top');
	const headerRef = useRef<HTMLElement>(null);

	const calculateScrollState = () => {
		const heroSection = document.getElementById('hero');
		const headerHeight = headerRef.current?.offsetHeight || 0;
		const heroBottom = heroSection ? heroSection.offsetTop + heroSection.offsetHeight - headerHeight / 2 : 0;

		if (window.scrollY === 0) {
			return 'top';
		} else if (window.scrollY > 0 && window.scrollY < heroBottom) {
			return 'scrolled-in-hero';
		} else {
			return 'scrolled-past-hero';
		}
	};

	useEffect(() => {
		setScrollState(calculateScrollState());

		const handleScroll = () => {
			setScrollState(calculateScrollState());
		};

		window.addEventListener('scroll', handleScroll);
		return () => window.removeEventListener('scroll', handleScroll);
	}, []);
	return (
		<header
			ref={headerRef}
			className={cn('fixed top-0 right-0 left-0 z-50 bg-transparent transition-all duration-300', {
				'bg-white/30 backdrop-blur-md': scrollState === 'scrolled-in-hero',
				'bg-white shadow-md': scrollState === 'scrolled-past-hero',
			})}
		>
			<div className='container mx-auto flex items-center justify-between px-6 py-4'>
				<Link
					href='/'
					className={cn('text-2xl font-bold text-white transition-colors duration-300', {
						'text-blue-600': scrollState === 'scrolled-past-hero',
					})}
				>
					{appName}
				</Link>
				<nav className='hidden space-x-4 md:flex'>
					{marketingNavItems.map((item) => (
						<Link
							key={item}
							href={`#${item}`}
							scroll={false}
							onClick={(e) => {
								e.preventDefault();
								document.getElementById(item)?.scrollIntoView({ behavior: 'smooth' });
							}}
							className={cn('text-white transition-colors duration-300 hover:text-gray-200', {
								'text-gray-600 hover:text-blue-600': scrollState === 'scrolled-past-hero',
							})}
						>
							{item.charAt(0).toUpperCase() + item.slice(1)}
						</Link>
					))}
				</nav>
				<Link href='/client'>
					<Button variant='default' className='hover:scale-105'>
						<span className='text-white'>Get Started</span>
					</Button>
				</Link>
			</div>
		</header>
	);
}
