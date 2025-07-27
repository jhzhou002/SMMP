import { Request, Response, NextFunction } from 'express'
import { logger } from './logger'

export const errorHandler = (
  error: any,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  logger.error('Unhandled error:', {
    error: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method,
    ip: req.ip,
    userAgent: req.get('User-Agent')
  })

  if (res.headersSent) {
    return next(error)
  }

  const isDevelopment = process.env.NODE_ENV === 'development'

  res.status(error.status || 500).json({
    success: false,
    message: error.message || 'Internal Server Error',
    ...(isDevelopment && { 
      stack: error.stack,
      details: error 
    })
  })
}