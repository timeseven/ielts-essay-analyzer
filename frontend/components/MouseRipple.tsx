'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';

export default function MouseRipple() {
	const [ripples, setRipples] = useState<{ x: number; y: number; id: number }[]>([]);
	const rippleWidth = 100;
	const rippleHeight = 100;
	useEffect(() => {
		const handleClick = (e: MouseEvent) => {
			const newRipple = {
				x: e.clientX - rippleWidth / 2,
				y: e.clientY - rippleHeight / 2,
				id: Date.now(),
			};
			setRipples((prevRipples) => [...prevRipples, newRipple]);
		};

		window.addEventListener('click', handleClick);

		return () => {
			window.removeEventListener('click', handleClick);
		};
	}, []);

	return (
		<div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, pointerEvents: 'none', zIndex: 9999 }}>
			<AnimatePresence>
				{ripples.map((ripple) => (
					<motion.div
						key={ripple.id}
						initial={{ scale: 0, opacity: 0.5, x: ripple.x, y: ripple.y }}
						animate={{ scale: 1, opacity: 0 }}
						exit={{ opacity: 0 }}
						transition={{ duration: 0.5 }}
						style={{
							position: 'absolute',
							width: rippleWidth,
							height: rippleHeight,
							borderRadius: '50%',
							backgroundColor: 'rgba(255, 255, 255, 0.5)',
							transform: 'translate(-50%, -50%)',
						}}
					/>
				))}
			</AnimatePresence>
		</div>
	);
}
