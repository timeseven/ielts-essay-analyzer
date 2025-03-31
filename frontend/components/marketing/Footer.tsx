'use client';

import Link from 'next/link';
import { Facebook, Twitter, Instagram, Linkedin } from 'lucide-react';
import { appName } from '@/lib/consts';

export default function Footer() {
	return (
		<footer className='w-full bg-gray-800 py-12 text-white'>
			<div className='container mx-auto px-4 md:px-6'>
				<div className='grid grid-cols-1 gap-8 md:grid-cols-4'>
					<div className='col-span-2'>
						<h3 className='mb-4 text-lg font-semibold'>{appName}</h3>
						<p className='text-sm text-gray-400'>
							Improve your IELTS essay score with our AI-powered essay analysis tool.
						</p>
					</div>
					<div>
						<h4 className='mb-4 text-lg font-semibold'>Company</h4>
						<ul className='space-y-2'>
							<li>
								<Link href='/about-us' className='text-sm text-gray-400 hover:text-white'>
									About Us
								</Link>
							</li>
							<li>
								<Link href='/contact' className='text-sm text-gray-400 hover:text-white'>
									Contact
								</Link>
							</li>
						</ul>
					</div>
					<div>
						<h4 className='mb-4 text-lg font-semibold'>Connect</h4>
						<div className='flex space-x-4'>
							<Link href='#' className='text-gray-400 hover:text-white'>
								<Facebook className='h-6 w-6' />
							</Link>
							<Link href='#' className='text-gray-400 hover:text-white'>
								<Twitter className='h-6 w-6' />
							</Link>
							<Link href='#' className='text-gray-400 hover:text-white'>
								<Instagram className='h-6 w-6' />
							</Link>
							<Link href='#' className='text-gray-400 hover:text-white'>
								<Linkedin className='h-6 w-6' />
							</Link>
						</div>
					</div>
				</div>
				<div className='mt-8 border-t border-gray-700 pt-8 text-center'>
					<p className='text-sm text-gray-400'>
						&copy; {new Date().getFullYear()} {appName}. All rights reserved.
					</p>
				</div>
			</div>
		</footer>
	);
}
