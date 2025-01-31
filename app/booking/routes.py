#app/booking/routes.py
from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.booking import bp
from app.booking.models import Room, Booking
from datetime import datetime, date
from sqlalchemy import and_, not_, or_
from sqlalchemy.exc import SQLAlchemyError

@bp.route('/')
@login_required
def index():
    rooms = Room.query.filter_by(is_available=True).all()
    return render_template('booking/index.html', rooms=rooms)

@bp.route('/check_availability', methods=['GET'])
@login_required
def check_availability():
    try:
        check_in_str = request.args.get('check_in')
        check_out_str = request.args.get('check_out')
        
        if not check_in_str or not check_out_str:
            flash('Please provide both check-in and check-out dates')
            return redirect(url_for('booking.index'))
            
        check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        
        # Validate dates
        today = date.today()
        if check_in < today or check_out <= check_in:
            flash('Invalid dates selected')
            return redirect(url_for('booking.index'))

        # Find unavailable rooms for the given dates
        unavailable_rooms = db.session.query(Room).join(Booking).filter(
            and_(
                Booking.status == 'confirmed',
                not_(
                    or_(
                        Booking.check_out_date <= check_in,
                        Booking.check_in_date >= check_out
                    )
                )
            )
        ).all()
        
        # Get all available rooms
        available_rooms = Room.query.filter(
            and_(
                Room.is_available == True,
                ~Room.id.in_([r.id for r in unavailable_rooms])
            )
        ).all()
        
        # Group rooms by type
        grouped_rooms = {}
        for room in available_rooms:
            if room.room_type not in grouped_rooms:
                grouped_rooms[room.room_type] = []
            grouped_rooms[room.room_type].append({
                'id': room.id,
                'room_number': room.room_number,
                'price': room.price_per_night,
                'description': room.description
            })
        
        return render_template('booking/availability.html', 
                             rooms=grouped_rooms, 
                             check_in=check_in, 
                             check_out=check_out)
                             
    except ValueError:
        flash('Invalid date format')
        return redirect(url_for('booking.index'))

@bp.route('/book_room', methods=['POST'])
@login_required
def book_room():
    try:
        room_id = request.form.get('room_id')
        check_in_str = request.form.get('check_in')
        check_out_str = request.form.get('check_out')
        
        if not all([room_id, check_in_str, check_out_str]):
            flash('Missing required booking information')
            return redirect(url_for('booking.index'))
            
        check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        
        room = Room.query.get_or_404(room_id)
        
        # Verify room is still available
        existing_booking = Booking.query.filter(
            and_(
                Booking.room_id == room_id,
                Booking.status == 'confirmed',
                not_(
                    or_(
                        Booking.check_out_date <= check_in,
                        Booking.check_in_date >= check_out
                    )
                )
            )
        ).first()
        
        if existing_booking:
            flash('Sorry, this room is no longer available for the selected dates')
            return redirect(url_for('booking.check_availability', 
                                  check_in=check_in_str, 
                                  check_out=check_out_str))
        
        booking = Booking(
            user_id=current_user.id,
            room_id=room_id,
            check_in_date=check_in,
            check_out_date=check_out
        )
        booking.total_price = booking.calculate_total_price()
        
        db.session.add(booking)
        db.session.commit()
        flash('Booking confirmed successfully!')
        
    except (ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        flash('Error occurred while booking. Please try again.')
        
    return redirect(url_for('booking.my_bookings'))

@bp.route('/my_bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).order_by(Booking.booking_date.desc()).all()
    return render_template('booking/my_bookings.html', bookings=bookings)

@bp.route('/cancel_booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.user_id != current_user.id:
        abort(403)
    
    if booking.check_in_date <= date.today():
        flash('Cannot cancel a booking that has already started or ended')
        return redirect(url_for('booking.my_bookings'))
        
    try:
        booking.status = 'cancelled'
        db.session.commit()
        flash('Booking cancelled successfully')
    except SQLAlchemyError:
        db.session.rollback()
        flash('Error occurred while cancelling booking')
        
    return redirect(url_for('booking.my_bookings'))